from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "e2.cpp"
DATA_LINE = re.compile(
    r"^\s*(\d+)\s+([0-9]+(?:\.[0-9]+)?)\s+"
    r"([0-9]+(?:\.[0-9]+)?)\s+(-?[0-9]+(?:\.[0-9]+)?)%\s*$"
)
Result = tuple[int, float, float, float]


def load_cpp_results() -> list[Result]:
    compiler = shutil.which("g++")
    if compiler is None:
        raise RuntimeError("No se encontró g++; instala g++ para compilar e2.cpp.")

    with tempfile.TemporaryDirectory(prefix="tsp-e2-") as temporary_directory:
        executable = Path(temporary_directory) / "e2"
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

    results = [
        (int(match.group(1)), float(match.group(2)), float(match.group(3)), float(match.group(4)))
        for line in output.splitlines()
        if (match := DATA_LINE.match(line))
    ]
    if not results:
        raise RuntimeError("No se pudieron leer los resultados impresos por e2.cpp.")
    return results


def build_figure(results: list[Result], selected_origin: int) -> go.Figure:
    origins = [row[0] for row in results]
    nn_costs = [row[1] for row in results]
    improved_costs = [row[2] for row in results]
    improvements = [row[3] for row in results]
    figure = go.Figure()
    figure.add_trace(
        go.Bar(
            name="NN",
            x=origins,
            y=nn_costs,
            marker_color="#e5b84b",
            customdata=[[origin, percent] for origin, percent in zip(origins, improvements)],
            hovertemplate="Origen %{customdata[0]}<br>NN: %{y:.3f}<br>Mejora: %{customdata[1]:.2f}%<extra></extra>",
        )
    )
    figure.add_trace(
        go.Bar(
            name="NN + 2-opt",
            x=origins,
            y=improved_costs,
            marker_color="#197c78",
            customdata=[[origin, percent] for origin, percent in zip(origins, improvements)],
            hovertemplate="Origen %{customdata[0]}<br>NN + 2-opt: %{y:.3f}<br>Mejora: %{customdata[1]:.2f}%<extra></extra>",
        )
    )
    figure.add_vline(
        x=selected_origin,
        line={"color": "#d45b45", "width": 1.5, "dash": "dot"},
        annotation_text=f"Origen {selected_origin}",
        annotation_position="top",
        annotation_font={"size": 10, "color": "#d45b45"},
    )
    figure.update_layout(
        template="plotly_white",
        barmode="group",
        height=450,
        margin={"l": 65, "r": 20, "t": 35, "b": 52},
        paper_bgcolor="#f7f6f0",
        plot_bgcolor="#f7f6f0",
        clickmode="event+select",
        legend={"orientation": "h", "y": 1.08, "x": 0},
        xaxis={"title": "Ciudad de inicio", "dtick": 1, "gridcolor": "#e1e4df", "zeroline": False},
        yaxis={"title": "Costo del ciclo", "gridcolor": "#d9dfdc", "zeroline": False},
        uirevision="e2-nn-2opt",
    )
    return figure


def create_png(results: list[Result], output: Path) -> None:
    origins = [row[0] for row in results]
    nn_costs = [row[1] for row in results]
    improved_costs = [row[2] for row in results]
    improvements = [row[3] for row in results]
    best_reduction = max(results, key=lambda row: row[3])
    average_reduction = sum(improvements) / len(improvements)
    x_positions = list(range(len(origins)))
    width = 0.38

    figure, (cost_axis, improvement_axis) = plt.subplots(
        2,
        1,
        figsize=(11, 7.5),
        sharex=True,
        gridspec_kw={"height_ratios": [2.2, 1]},
    )
    figure.patch.set_facecolor("#f7f6f0")
    for axis in (cost_axis, improvement_axis):
        axis.set_facecolor("#f7f6f0")
        axis.grid(axis="y", color="#d9dfdc", linewidth=0.7)
        axis.set_axisbelow(True)
        axis.spines[["top", "right"]].set_visible(False)

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
        improved_costs,
        width,
        label="NN + 2-opt",
        color="#197c78",
        edgecolor="#263238",
        linewidth=0.5,
    )
    cost_axis.set_ylabel("Costo del ciclo")
    cost_axis.set_title("e2 · Efecto de 2-opt según el origen", loc="left", fontsize=14, fontweight="bold", pad=12)
    cost_axis.legend(frameon=False, loc="upper right", ncol=2)
    cost_axis.text(
        0.01,
        0.98,
        f"Mejora media: {average_reduction:.2f}%     Mayor mejora: {best_reduction[3]:.2f}% (origen {best_reduction[0]})",
        transform=cost_axis.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        color="#465458",
    )

    colors = ["#d45b45" if row[0] == best_reduction[0] else "#327b87" for row in results]
    improvement_axis.bar(
        x_positions,
        improvements,
        color=colors,
        edgecolor="#263238",
        linewidth=0.5,
    )
    improvement_axis.axhline(
        average_reduction,
        color="#263238",
        linewidth=1.2,
        linestyle=(0, (3, 3)),
        label=f"Media: {average_reduction:.2f}%",
    )
    improvement_axis.set_ylabel("Reducción (%)")
    improvement_axis.set_xlabel("Ciudad de inicio")
    improvement_axis.set_xticks(x_positions, origins)
    improvement_axis.legend(frameon=False, loc="upper right")
    improvement_axis.margins(y=0.22)
    figure.tight_layout(h_pad=1.5)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(figure)
    print(f"Imagen guardada en: {output.resolve()}")


def create_app(results: list[Result]) -> Dash:
    origins = [row[0] for row in results]
    nn_costs = [row[1] for row in results]
    improved_costs = [row[2] for row in results]
    improvements = [row[3] for row in results]
    selected_origin = max(results, key=lambda row: row[3])[0]
    mean_nn = sum(nn_costs) / len(nn_costs)
    mean_2opt = sum(improved_costs) / len(improved_costs)
    mean_improvement = sum(improvements) / len(improvements)
    best_nn = min(nn_costs)
    best_2opt = min(improved_costs)
    improved_count = sum(after < before for before, after in zip(nn_costs, improved_costs))

    app = Dash(__name__)
    app.title = "TSP e2 | NN y 2-opt"
    app.layout = html.Main(
        [
            html.Header(
                [
                    html.P("TSP / EXPERIMENTO 02", className="eyebrow"),
                    html.H1("¿Cuánto mejora 2-opt la ruta NN?"),
                    html.P("Comparación del costo antes y después de la búsqueda local para cada ciudad de inicio."),
                ],
                className="header",
            ),
            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H2("Costo por origen"),
                                    html.Span("Haz clic en una barra para comparar el caso", className="graph-meta"),
                                ],
                                className="graph-heading",
                            ),
                            dcc.Graph(
                                id="comparison-chart",
                                figure=build_figure(results, selected_origin),
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
                                [html.Span("NN + 2-opt", className="metric-label"), html.Strong("", id="two-opt-cost", className="metric-value")],
                                className="metric-row",
                            ),
                            html.Div(
                                [html.Span("Ahorro", className="metric-label"), html.Strong("", id="selected-saving", className="metric-value")],
                                className="metric-row highlight-row",
                            ),
                            html.P(id="selected-description", className="note"),
                            html.Div(className="summary-divider"),
                            html.P("RESUMEN DE LOS 15 ORÍGENES", className="eyebrow"),
                            html.Div(
                                [html.Span("Costo medio", className="metric-label"), html.Strong(f"{mean_nn:.2f} → {mean_2opt:.2f}", className="metric-value")],
                                className="metric-row",
                            ),
                            html.Div(
                                [html.Span("Reducción media", className="metric-label"), html.Strong(f"{mean_improvement:.2f}%", className="metric-value")],
                                className="metric-row",
                            ),
                            html.Div(
                                [html.Span("Orígenes mejorados", className="metric-label"), html.Strong(f"{improved_count} / {len(results)}", className="metric-value")],
                                className="metric-row",
                            ),
                            html.Div(
                                [html.Span("Mejor costo 2-opt", className="metric-label"), html.Strong(f"{best_2opt:.3f}", className="metric-value")],
                                className="metric-row",
                            ),
                        ],
                        className="summary-panel",
                    ),
                ],
                className="workspace",
            ),
            html.Footer("Compilado y calculado desde e2.cpp · misma instancia determinista de 15 ciudades", className="footer"),
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
      .page { max-width: 1280px; margin: 0 auto; padding: 38px 42px 24px; }
      .header { border-bottom: 1px solid var(--line); padding-bottom: 24px; }
      .eyebrow { margin: 0 0 9px; color: var(--accent); font: 500 11px 'DM Mono', monospace; }
      h1 { margin: 0; font-size: 32px; line-height: 1.15; font-weight: 800; }
      .header > p:last-child { margin: 8px 0 0; color: var(--muted); font-size: 14px; }
      .workspace { display: grid; grid-template-columns: minmax(0, 1fr) 310px; gap: 34px; align-items: start; padding-top: 24px; }
      .chart-panel { min-width: 0; }
      .graph-heading { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; padding: 0 8px; }
      h2 { margin: 0; font-size: 16px; }
      .graph-meta { color: var(--muted); font: 11px 'DM Mono', monospace; }
      .summary-panel { border-left: 1px solid var(--line); padding: 10px 0 8px 24px; }
      .selected-origin { margin: 18px 0 12px; font-size: 19px; font-weight: 700; }
      .metric-row { display: flex; justify-content: space-between; gap: 10px; align-items: baseline; border-top: 1px solid var(--line); padding: 12px 0 10px; }
      .metric-label { color: var(--muted); font-size: 12px; }
      .metric-value { font: 500 12px 'DM Mono', monospace; text-align: right; }
      .highlight-row .metric-value { color: #197c78; }
      .note { margin: 14px 0 18px; color: var(--muted); font-size: 12px; line-height: 1.6; }
      .summary-divider { border-top: 1px solid var(--line); margin: 18px 0; }
      .footer { margin-top: 20px; border-top: 1px solid var(--line); padding-top: 15px; color: var(--muted); font: 10px 'DM Mono', monospace; }
      @media (max-width: 760px) {
        .page { padding: 24px 18px 20px; }
        h1 { font-size: 25px; }
        .workspace { grid-template-columns: 1fr; gap: 12px; }
        .summary-panel { border-left: 0; border-top: 1px solid var(--line); padding: 22px 4px 4px; }
      }
    </style>
  </head>
  <body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer></body>
</html>"""

    @app.callback(
        Output("selected-origin", "children"),
        Output("nn-cost", "children"),
        Output("two-opt-cost", "children"),
        Output("selected-saving", "children"),
        Output("selected-description", "children"),
        Output("comparison-chart", "figure"),
        Input("comparison-chart", "clickData"),
    )
    def select_origin(click_data: dict[str, object] | None) -> tuple[str, str, str, str, str, go.Figure]:
        origin = selected_origin
        if click_data and click_data.get("points"):
            origin = int(click_data["points"][0]["x"])
        row = next(item for item in results if item[0] == origin)
        _, before, after, percentage = row
        saving = before - after
        return (
            f"Ciudad {origin}",
            f"{before:.3f}",
            f"{after:.3f}",
            f"{saving:.3f} ({percentage:.2f}%)",
            "2-opt reduce el costo de este origen." if saving > 0 else "2-opt no cambió el costo de este origen.",
            build_figure(results, origin),
        )

    return app


def main() -> None:
    results = load_cpp_results()
    create_png(results, HERE / "e2_comparacion_nn_2opt.png")
    app = create_app(results)
    print(f"Orígenes: {len(results)}")
    print(f"Mejora media: {sum(row[3] for row in results) / len(results):.2f}%")
    print(f"Mayor mejora: origen {max(results, key=lambda row: row[3])[0]}")
    app.run(debug=False, port=8053)


if __name__ == "__main__":
    main()
