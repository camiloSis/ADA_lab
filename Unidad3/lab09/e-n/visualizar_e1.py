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
SOURCE = HERE / "e1.cpp"
DATA_LINE = re.compile(r"^\s*(\d+)\s+([0-9]+(?:\.[0-9]+)?)\s*$")


def load_cpp_results() -> list[tuple[int, float]]:
    compiler = shutil.which("g++")
    if compiler is None:
        raise RuntimeError("No se encontró g++; instala g++ para compilar e1.cpp.")

    with tempfile.TemporaryDirectory(prefix="tsp-e1-") as temporary_directory:
        executable = Path(temporary_directory) / "e1"
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
        (int(match.group(1)), float(match.group(2)))
        for line in output.splitlines()
        if (match := DATA_LINE.match(line))
    ]
    if not results:
        raise RuntimeError("No se pudieron leer los costos impresos por e1.cpp.")
    return results


def build_figure(results: list[tuple[int, float]], selected_origin: int) -> go.Figure:
    origins = [origin for origin, _ in results]
    costs = [cost for _, cost in results]
    best_cost = min(costs)
    mean_cost = sum(costs) / len(costs)
    colors = [
        "#d45b45" if origin == selected_origin else "#197c78" if cost == best_cost else "#e5b84b"
        for origin, cost in results
    ]
    figure = go.Figure(
        go.Bar(
            x=origins,
            y=costs,
            marker={"color": colors, "line": {"color": "#263238", "width": 0.6}},
            customdata=[[origin, cost - best_cost] for origin, cost in results],
            hovertemplate=(
                "Origen %{customdata[0]}<br>"
                "Costo NN: %{y:.3f}<br>"
                "Sobre el mejor: %{customdata[1]:.3f}<extra></extra>"
            ),
        )
    )
    figure.add_hline(
        y=mean_cost,
        line={"color": "#263238", "width": 1.5, "dash": "dot"},
        annotation_text=f"Media {mean_cost:.2f}",
        annotation_position="top left",
        annotation_font={"size": 11, "color": "#263238"},
    )
    figure.update_layout(
        template="plotly_white",
        height=470,
        margin={"l": 65, "r": 24, "t": 35, "b": 52},
        paper_bgcolor="#f7f6f0",
        plot_bgcolor="#f7f6f0",
        clickmode="event+select",
        showlegend=False,
        xaxis={
            "title": "Ciudad de inicio",
            "dtick": 1,
            "gridcolor": "#e1e4df",
            "zeroline": False,
        },
        yaxis={
            "title": "Costo del ciclo",
            "gridcolor": "#d9dfdc",
            "zeroline": False,
        },
        uirevision="e1-origin-costs",
    )
    return figure


def create_png(results: list[tuple[int, float]], output: Path) -> None:
    origins = [origin for origin, _ in results]
    costs = [cost for _, cost in results]
    best_cost = min(costs)
    best_origin = origins[costs.index(best_cost)]
    mean_cost = sum(costs) / len(costs)
    worst_cost = max(costs)
    colors = ["#197c78" if cost == best_cost else "#e5b84b" for cost in costs]

    figure, axis = plt.subplots(figsize=(10.5, 5.4))
    figure.patch.set_facecolor("#f7f6f0")
    axis.set_facecolor("#f7f6f0")
    bars = axis.bar(origins, costs, color=colors, edgecolor="#263238", linewidth=0.6)
    axis.axhline(mean_cost, color="#263238", linewidth=1.3, linestyle=(0, (3, 3)), label=f"Media: {mean_cost:.2f}")
    axis.bar_label(bars, fmt="%.1f", padding=3, fontsize=8, color="#263238")
    axis.set_title("e1 · Costo de Nearest Neighbor según el origen", loc="left", fontsize=14, fontweight="bold", pad=15)
    axis.set_xlabel("Ciudad de inicio")
    axis.set_ylabel("Costo del ciclo")
    axis.set_xticks(origins)
    axis.grid(axis="y", color="#d9dfdc", linewidth=0.7)
    axis.set_axisbelow(True)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(frameon=False, loc="upper right")
    axis.text(
        0.01,
        0.98,
        f"Mejor: {best_cost:.2f} (origen {best_origin})     Peor: {worst_cost:.2f}     Media: {mean_cost:.2f}",
        transform=axis.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        color="#465458",
    )
    axis.margins(y=0.18)
    figure.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(figure)
    print(f"Imagen guardada en: {output.resolve()}")


def create_app(results: list[tuple[int, float]]) -> Dash:
    origins = [origin for origin, _ in results]
    costs = [cost for _, cost in results]
    best_cost = min(costs)
    worst_cost = max(costs)
    mean_cost = sum(costs) / len(costs)
    best_origin = origins[costs.index(best_cost)]
    spread_percent = 100 * (worst_cost - best_cost) / best_cost

    app = Dash(__name__)
    app.title = "TSP e1 | Influencia del origen"
    app.layout = html.Main(
        [
            html.Header(
                [
                    html.P("TSP / EXPERIMENTO 01", className="eyebrow"),
                    html.H1("¿Desde dónde conviene empezar?"),
                    html.P("Costo del ciclo Nearest Neighbor para cada ciudad de origen, sobre la misma instancia de 15 ciudades."),
                ],
                className="header",
            ),
            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H2("Costo por ciudad de inicio"),
                                    html.Span("Haz clic en una barra para inspeccionarla", className="graph-meta"),
                                ],
                                className="graph-heading",
                            ),
                            dcc.Graph(
                                id="origin-chart",
                                figure=build_figure(results, best_origin),
                                config={"displayModeBar": False, "responsive": True},
                                clickData={"points": [{"x": best_origin}]},
                            ),
                        ],
                        className="chart-panel",
                    ),
                    html.Aside(
                        [
                            html.P("ORIGEN SELECCIONADO", className="eyebrow"),
                            html.Div(f"Ciudad {best_origin}", id="selected-origin", className="selected-origin"),
                            html.Div(f"{best_cost:.3f}", id="selected-cost", className="selected-cost"),
                            html.P("Costo del ciclo cerrado", className="selected-caption"),
                            html.Div(
                                [html.Span("Mejor", className="metric-label"), html.Strong(f"{best_cost:.3f} · origen {best_origin}", className="metric-value")],
                                className="metric-row",
                            ),
                            html.Div(
                                [html.Span("Peor", className="metric-label"), html.Strong(f"{worst_cost:.3f}", className="metric-value")],
                                className="metric-row",
                            ),
                            html.Div(
                                [html.Span("Media", className="metric-label"), html.Strong(f"{mean_cost:.3f}", className="metric-value")],
                                className="metric-row",
                            ),
                            html.Div(
                                [html.Span("Rango relativo", className="metric-label"), html.Strong(f"{spread_percent:.1f}%", className="metric-value")],
                                className="metric-row",
                            ),
                            html.P(id="selected-difference", className="note"),
                        ],
                        className="summary-panel",
                    ),
                ],
                className="workspace",
            ),
            html.Footer("Compilado y calculado desde e1.cpp · generador determinista con semilla 42", className="footer"),
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
      .workspace { display: grid; grid-template-columns: minmax(0, 1fr) 280px; gap: 34px; align-items: start; padding-top: 24px; }
      .chart-panel { min-width: 0; }
      .graph-heading { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; padding: 0 8px; }
      h2 { margin: 0; font-size: 16px; }
      .graph-meta { color: var(--muted); font: 11px 'DM Mono', monospace; }
      .summary-panel { border-left: 1px solid var(--line); padding: 10px 0 8px 24px; }
      .selected-origin { margin-top: 26px; font-size: 18px; font-weight: 700; }
      .selected-cost { margin-top: 8px; font: 500 34px 'DM Mono', monospace; color: #197c78; }
      .selected-caption { margin: 4px 0 26px; color: var(--muted); font-size: 12px; }
      .metric-row { display: flex; justify-content: space-between; gap: 12px; align-items: baseline; border-top: 1px solid var(--line); padding: 14px 0 11px; }
      .metric-label { color: var(--muted); font-size: 12px; }
      .metric-value { font: 500 12px 'DM Mono', monospace; text-align: right; }
      .note { margin-top: 20px; color: var(--muted); font-size: 12px; line-height: 1.6; }
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
        Output("selected-cost", "children"),
        Output("selected-difference", "children"),
        Output("origin-chart", "figure"),
        Input("origin-chart", "clickData"),
    )
    def select_origin(click_data: dict[str, object] | None) -> tuple[str, str, str, go.Figure]:
        origin = best_origin
        if click_data and click_data.get("points"):
            origin = int(click_data["points"][0]["x"])
        cost = costs[origins.index(origin)]
        difference = cost - best_cost
        if difference == 0:
            detail = "Este origen alcanza el menor costo observado en esta instancia."
        else:
            detail = f"Este inicio cuesta {difference:.3f} ({100 * difference / best_cost:.1f}%) más que el mejor resultado."
        return f"Ciudad {origin}", f"{cost:.3f}", detail, build_figure(results, origin)

    return app


def main() -> None:
    results = load_cpp_results()
    create_png(results, HERE / "e1_costo_por_origen.png")
    app = create_app(results)
    print(f"Resultados de {len(results)} orígenes; mejor costo: {min(cost for _, cost in results):.3f}")
    app.run(debug=False, port=8052)


if __name__ == "__main__":
    main()
