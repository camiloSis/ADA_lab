from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from plotly.subplots import make_subplots


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "e3.cpp"
DATA_LINE = re.compile(
    r"^\s*(\d+)\s+([0-9]+(?:\.[0-9]+)?)\s+"
    r"([0-9]+(?:\.[0-9]+)?)\s+(CI|NN|empate)\s*$"
)
SUMMARY_LINE = re.compile(
    r"^\s*(NN|Ins\. barata)\s+([0-9]+(?:\.[0-9]+)?)\s+"
    r"([0-9]+(?:\.[0-9]+)?)\s+([0-9]+(?:\.[0-9]+)?)\s+"
    r"(\d+)/15\s+(\d+)\s+([0-9]+(?:\.[0-9]+)?)\s*$"
)
MEAN_IMPROVEMENT_LINE = re.compile(r"Mejora media de CI sobre NN:\s*([0-9]+(?:\.[0-9]+)?)%")
TIME_RATIO_LINE = re.compile(r"CI es\s*([0-9]+(?:\.[0-9]+)?)\s*veces más lenta")
Result = tuple[int, float, float, str]
Stats = dict[str, tuple[float, float, float, int, int, float]]


def load_cpp_results() -> tuple[list[Result], Stats, float, float]:
    compiler = shutil.which("g++")
    if compiler is None:
        raise RuntimeError("No se encontró g++; instala g++ para compilar e3.cpp.")

    with tempfile.TemporaryDirectory(prefix="tsp-e3-") as temporary_directory:
        executable = Path(temporary_directory) / "e3"
        subprocess.run(
            [compiler, "-std=c++17", "-O2", str(SOURCE), "-o", str(executable)],
            check=True,
            cwd=HERE,
        )
        output = subprocess.run(
            [str(executable)],
            check=True,
            capture_output=True,
            text=True,
            cwd=HERE,
        ).stdout

    results: list[Result] = []
    stats: Stats = {}
    mean_improvement = None
    time_ratio = None
    for line in output.splitlines():
        if match := DATA_LINE.match(line):
            results.append((int(match.group(1)), float(match.group(2)), float(match.group(3)), match.group(4)))
        elif match := SUMMARY_LINE.match(line):
            stats[match.group(1)] = (
                float(match.group(2)),
                float(match.group(3)),
                float(match.group(4)),
                int(match.group(5)),
                int(match.group(6)),
                float(match.group(7)),
            )
        elif match := MEAN_IMPROVEMENT_LINE.search(line):
            mean_improvement = float(match.group(1))
        elif match := TIME_RATIO_LINE.search(line):
            time_ratio = float(match.group(1))

    if len(results) != 15 or len(stats) != 2 or mean_improvement is None or time_ratio is None:
        raise RuntimeError("No se pudo interpretar toda la tabla de resultados de e3.cpp.")
    return results, stats, mean_improvement, time_ratio


def build_figure(
    results: list[Result],
    stats: Stats,
    selected_origin: int,
    mean_improvement: float,
) -> go.Figure:
    origins = [row[0] for row in results]
    nn_costs = [row[1] for row in results]
    insertion_costs = [row[2] for row in results]
    winners = [row[3] for row in results]
    relative_changes = [(nn - insertion) / nn * 100 for nn, insertion in zip(nn_costs, insertion_costs)]
    nn_time = stats["NN"][5]
    insertion_time = stats["Ins. barata"][5]

    figure = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=False,
        vertical_spacing=0.16,
        row_heights=[0.49, 0.29, 0.22],
        subplot_titles=("Costo del ciclo por origen", "Variación de inserción barata respecto a NN", "Tiempo medio medido"),
    )
    figure.add_trace(
        go.Bar(
            name="NN",
            x=origins,
            y=nn_costs,
            marker_color="#e5b84b",
            customdata=[[winner, insertion] for winner, insertion in zip(winners, insertion_costs)],
            hovertemplate="Origen %{x}<br>NN: %{y:.3f}<br>Inserción barata: %{customdata[1]:.3f}<br>Gana: %{customdata[0]}<extra></extra>",
        ),
        row=1,
        col=1,
    )
    figure.add_trace(
        go.Bar(
            name="Inserción barata",
            x=origins,
            y=insertion_costs,
            marker_color="#197c78",
            customdata=[[winner, nn] for winner, nn in zip(winners, nn_costs)],
            hovertemplate="Origen %{x}<br>Inserción barata: %{y:.3f}<br>NN: %{customdata[1]:.3f}<br>Gana: %{customdata[0]}<extra></extra>",
        ),
        row=1,
        col=1,
    )
    figure.add_trace(
        go.Bar(
            name="Ahorro (+) / sobrecosto (-)",
            x=origins,
            y=relative_changes,
            marker_color=["#197c78" if value >= 0 else "#d45b45" for value in relative_changes],
            hovertemplate="Origen %{x}<br>Variación frente a NN: %{y:.2f}%<extra></extra>",
            showlegend=False,
        ),
        row=2,
        col=1,
    )
    figure.add_hline(y=0, line={"color": "#263238", "width": 1}, row=2, col=1)
    figure.add_trace(
        go.Bar(
            name="Tiempo medio (ms)",
            x=["NN", "Inserción barata"],
            y=[nn_time, insertion_time],
            marker_color=["#e5b84b", "#197c78"],
            text=[f"{nn_time:.4f} ms", f"{insertion_time:.4f} ms"],
            textposition="outside",
            hovertemplate="%{x}<br>Tiempo medio: %{y:.4f} ms<extra></extra>",
            showlegend=False,
        ),
        row=3,
        col=1,
    )

    figure.add_vline(
        x=selected_origin,
        line={"color": "#d45b45", "width": 1.4, "dash": "dot"},
        row=1,
        col=1,
    )
    figure.update_layout(
        template="plotly_white",
        barmode="group",
        height=800,
        margin={"l": 65, "r": 20, "t": 75, "b": 48},
        paper_bgcolor="#f7f6f0",
        plot_bgcolor="#f7f6f0",
        clickmode="event+select",
        legend={"orientation": "h", "y": 1.08, "x": 0},
        xaxis={"dtick": 1, "gridcolor": "#e1e4df", "zeroline": False},
        xaxis2={"title": "Ciudad de inicio", "dtick": 1, "gridcolor": "#e1e4df", "zeroline": False},
        xaxis3={"gridcolor": "#e1e4df", "zeroline": False},
        yaxis={"title": "Costo", "gridcolor": "#d9dfdc", "zeroline": False},
        yaxis2={"title": "Variación (%)", "gridcolor": "#d9dfdc", "zeroline": False},
        yaxis3={"title": "Milisegundos", "gridcolor": "#d9dfdc", "zeroline": False},
        uirevision="e3-nn-insertion",
    )
    for annotation in figure.layout.annotations:
        annotation.font = {"size": 12, "color": "#465458"}
    return figure


def create_png(
    results: list[Result],
    stats: Stats,
    mean_improvement: float,
    time_ratio: float,
    output: Path,
) -> None:
    origins = [row[0] for row in results]
    nn_costs = [row[1] for row in results]
    insertion_costs = [row[2] for row in results]
    relative_changes = [(nn - insertion) / nn * 100 for nn, insertion in zip(nn_costs, insertion_costs)]
    winner_counts = {winner: sum(row[3] == winner for row in results) for winner in ("CI", "NN", "empate")}
    x_positions = list(range(len(origins)))
    width = 0.38

    figure, axes = plt.subplots(
        3,
        1,
        figsize=(11, 9.5),
        gridspec_kw={"height_ratios": [2.2, 1.3, 1]},
    )
    figure.patch.set_facecolor("#f7f6f0")
    for axis in axes:
        axis.set_facecolor("#f7f6f0")
        axis.grid(axis="y", color="#d9dfdc", linewidth=0.7)
        axis.set_axisbelow(True)
        axis.spines[["top", "right"]].set_visible(False)

    cost_axis, change_axis, time_axis = axes
    cost_axis.bar(
        [position - width / 2 for position in x_positions],
        nn_costs,
        width,
        label="NN",
        color="#e5b84b",
        edgecolor="#263238",
        linewidth=0.5,
    )
    cost_axis.bar(
        [position + width / 2 for position in x_positions],
        insertion_costs,
        width,
        label="Inserción barata",
        color="#197c78",
        edgecolor="#263238",
        linewidth=0.5,
    )
    cost_axis.set_ylabel("Costo del ciclo")
    cost_axis.set_title("e3 · NN frente a inserción barata", loc="left", fontsize=14, fontweight="bold", pad=12)
    cost_axis.legend(frameon=False, loc="upper right", ncol=2)
    cost_axis.text(
        0.01,
        0.98,
        f"Gana inserción: {winner_counts['CI']}     Gana NN: {winner_counts['NN']}     Empates: {winner_counts['empate']}",
        transform=cost_axis.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        color="#465458",
    )

    change_colors = ["#197c78" if value >= 0 else "#d45b45" for value in relative_changes]
    change_axis.bar(x_positions, relative_changes, color=change_colors, edgecolor="#263238", linewidth=0.5)
    change_axis.axhline(0, color="#263238", linewidth=1)
    change_axis.set_ylabel("Ahorro (+) / sobrecosto (-) (%)")
    change_axis.text(
        0.01,
        0.98,
        f"Reducción media de costos reportada por e3: {mean_improvement:.2f}%",
        transform=change_axis.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        color="#465458",
    )

    times = [stats["NN"][5], stats["Ins. barata"][5]]
    time_bars = time_axis.bar(
        ["NN", "Inserción barata"],
        times,
        color=["#e5b84b", "#197c78"],
        edgecolor="#263238",
        linewidth=0.6,
    )
    time_axis.bar_label(time_bars, labels=[f"{value:.4f} ms" for value in times], padding=3, fontsize=9)
    time_axis.set_ylabel("Tiempo medio (ms)")
    time_axis.set_xlabel("Heurística")
    time_axis.text(
        0.99,
        0.98,
        f"Inserción barata: {time_ratio:.1f}× más lenta en esta medición",
        transform=time_axis.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        color="#465458",
    )
    time_axis.margins(y=0.28)
    figure.tight_layout(h_pad=1.5)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(figure)
    print(f"Imagen guardada en: {output.resolve()}")


def create_app(
    results: list[Result],
    stats: Stats,
    mean_improvement: float,
    time_ratio: float,
) -> Dash:
    nn_costs = [row[1] for row in results]
    insertion_costs = [row[2] for row in results]
    winners = [row[3] for row in results]
    selected_origin = max(results, key=lambda row: row[1] - row[2])[0]
    winner_counts = {winner: sum(value == winner for value in winners) for winner in ("CI", "NN", "empate")}
    nn_stats = stats["NN"]
    insertion_stats = stats["Ins. barata"]

    app = Dash(__name__)
    app.title = "TSP e3 | NN e inserción barata"
    app.layout = html.Main(
        [
            html.Header(
                [
                    html.P("TSP / EXPERIMENTO 03", className="eyebrow"),
                    html.H1("Calidad de ruta y costo de ejecución"),
                    html.P("Comparación de Nearest Neighbor e inserción barata sobre los mismos 15 orígenes."),
                ],
                className="header",
            ),
            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H2("Resultados de las heurísticas"),
                                    html.Span("Haz clic en un origen para inspeccionar sus costos", className="graph-meta"),
                                ],
                                className="graph-heading",
                            ),
                            dcc.Graph(
                                id="comparison-chart",
                                figure=build_figure(results, stats, selected_origin, mean_improvement),
                                config={"displayModeBar": False, "responsive": True},
                                clickData={"points": [{"x": selected_origin}]},
                            ),
                        ],
                        className="chart-panel",
                    ),
                    html.Aside(
                        [
                            html.P("ORIGEN SELECCIONADO", className="eyebrow"),
                            html.Div(f"Ciudad {selected_origin}", id="selected-origin", className="selected-origin"),
                            html.Div(
                                [html.Span("NN", className="metric-label"), html.Strong("", id="nn-cost", className="metric-value")],
                                className="metric-row",
                            ),
                            html.Div(
                                [html.Span("Inserción barata", className="metric-label"), html.Strong("", id="insertion-cost", className="metric-value")],
                                className="metric-row",
                            ),
                            html.Div(
                                [html.Span("Ganador", className="metric-label"), html.Strong("", id="selected-winner", className="metric-value")],
                                className="metric-row highlight-row",
                            ),
                            html.P(id="selected-change", className="note"),
                            html.Div(className="summary-divider"),
                            html.P("RESUMEN DE LA MUESTRA", className="eyebrow"),
                            html.Div(
                                [html.Span("Costo medio", className="metric-label"), html.Strong(f"{nn_stats[2]:.2f} → {insertion_stats[2]:.2f}", className="metric-value")],
                                className="metric-row",
                            ),
                            html.Div(
                                [html.Span("Gana CI / NN", className="metric-label"), html.Strong(f"{winner_counts['CI']} / {winner_counts['NN']}", className="metric-value")],
                                className="metric-row",
                            ),
                            html.Div(
                                [html.Span("Tiempo NN", className="metric-label"), html.Strong(f"{nn_stats[5]:.4f} ms", className="metric-value")],
                                className="metric-row",
                            ),
                            html.Div(
                                [html.Span("Tiempo CI", className="metric-label"), html.Strong(f"{insertion_stats[5]:.4f} ms", className="metric-value")],
                                className="metric-row",
                            ),
                            html.Div(
                                [html.Span("Relación de tiempos", className="metric-label"), html.Strong(f"{time_ratio:.1f}×", className="metric-value")],
                                className="metric-row",
                            ),
                            html.P(f"Reducción media del costo con CI: {mean_improvement:.2f}%.", className="note"),
                        ],
                        className="summary-panel",
                    ),
                ],
                className="workspace",
            ),
            html.Footer("Compilado y calculado desde e3.cpp · tiempos de una medición local", className="footer"),
        ],
        className="page",
    )
    app.index_string = """<!DOCTYPE html>
<html>
  <head>
    {%metas%}<title>{%title%}</title>{%favicon%}{%css%}
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
      :root { color-scheme: light; --ink: #17252a; --muted: #647276; --line: #d7ddda; --paper: #f7f6f0; --accent: #d45b45; }
      * { box-sizing: border-box; }
      body { margin: 0; background: var(--paper); color: var(--ink); font-family: 'Manrope', sans-serif; }
      .page { max-width: 1440px; margin: 0 auto; padding: 34px 36px 22px; }
      .header { border-bottom: 1px solid var(--line); padding-bottom: 20px; }
      .eyebrow { margin: 0 0 8px; color: var(--accent); font: 500 11px 'DM Mono', monospace; }
      h1 { margin: 0; font-size: 30px; line-height: 1.15; font-weight: 800; }
      .header > p:last-child { margin: 8px 0 0; color: var(--muted); font-size: 13px; }
      .workspace { display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 28px; align-items: start; padding-top: 20px; }
      .chart-panel { min-width: 0; }
      .graph-heading { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; padding: 0 8px; }
      h2 { margin: 0; font-size: 16px; }
      .graph-meta { color: var(--muted); font: 11px 'DM Mono', monospace; }
      .summary-panel { border-left: 1px solid var(--line); padding: 8px 0 6px 22px; }
      .selected-origin { margin: 16px 0 10px; font-size: 18px; font-weight: 700; }
      .metric-row { display: flex; justify-content: space-between; gap: 8px; align-items: baseline; border-top: 1px solid var(--line); padding: 10px 0 8px; }
      .metric-label { color: var(--muted); font-size: 11px; }
      .metric-value { font: 500 11px 'DM Mono', monospace; text-align: right; }
      .highlight-row .metric-value { color: #197c78; }
      .note { margin: 12px 0 14px; color: var(--muted); font-size: 11px; line-height: 1.55; }
      .summary-divider { border-top: 1px solid var(--line); margin: 14px 0; }
      .footer { margin-top: 16px; border-top: 1px solid var(--line); padding-top: 12px; color: var(--muted); font: 10px 'DM Mono', monospace; }
      @media (max-width: 900px) {
        .page { padding: 24px 18px 20px; }
        h1 { font-size: 25px; }
        .workspace { grid-template-columns: 1fr; gap: 8px; }
        .summary-panel { border-left: 0; border-top: 1px solid var(--line); padding: 20px 4px 4px; }
      }
    </style>
  </head>
  <body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer></body>
</html>"""

    @app.callback(
        Output("selected-origin", "children"),
        Output("nn-cost", "children"),
        Output("insertion-cost", "children"),
        Output("selected-winner", "children"),
        Output("selected-change", "children"),
        Output("comparison-chart", "figure"),
        Input("comparison-chart", "clickData"),
    )
    def select_origin(click_data: dict[str, object] | None) -> tuple[str, str, str, str, str, go.Figure]:
        origin = selected_origin
        if click_data and click_data.get("points"):
            try:
                origin = int(click_data["points"][0]["x"])
            except (TypeError, ValueError):
                pass
        row = next(item for item in results if item[0] == origin)
        _, nn, insertion, winner = row
        change = (nn - insertion) / nn * 100
        detail = (
            f"Inserción barata reduce el costo en {change:.2f}%."
            if change > 0
            else f"Inserción barata aumenta el costo en {abs(change):.2f}%."
            if change < 0
            else "Ambas heurísticas producen el mismo costo."
        )
        winner_label = {"CI": "Inserción barata", "NN": "NN", "empate": "Empate"}[winner]
        return (
            f"Ciudad {origin}",
            f"{nn:.3f}",
            f"{insertion:.3f}",
            winner_label,
            detail,
            build_figure(results, stats, origin, mean_improvement),
        )

    return app


def main() -> None:
    results, stats, mean_improvement, time_ratio = load_cpp_results()
    create_png(
        results,
        stats,
        mean_improvement,
        time_ratio,
        HERE / "e3_comparacion_nn_insercion.png",
    )
    app = create_app(results, stats, mean_improvement, time_ratio)
    print(f"Orígenes: {len(results)}")
    print(f"Mejora media de costo: {mean_improvement:.2f}%")
    print(f"Relación de tiempos CI/NN: {time_ratio:.1f}x")
    app.run(debug=False, port=8054)


if __name__ == "__main__":
    main()
