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
SOURCE = HERE / "e4.cpp"
NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
ROW_PATTERN = re.compile(
    rf"^\s*(\d+)\s+({NUMBER})\s+({NUMBER})\s+({NUMBER})\s+"
    rf"({NUMBER})\s+({NUMBER})\s+({NUMBER})\s*$"
)
Result = tuple[int, float, float, float, float, float, float]
AGE_OF_UNIVERSE_YEARS = 1.38e10


def load_cpp_results() -> list[Result]:
    compiler = shutil.which("g++")
    if compiler is None:
        raise RuntimeError("No se encontró g++; instala g++ para compilar e4.cpp.")

    with tempfile.TemporaryDirectory(prefix="tsp-e4-") as temporary_directory:
        executable = Path(temporary_directory) / "e4"
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
        (
            int(match.group(1)),
            float(match.group(2)),
            float(match.group(3)),
            float(match.group(4)),
            float(match.group(5)),
            float(match.group(6)),
            float(match.group(7)),
        )
        for line in output.splitlines()
        if (match := ROW_PATTERN.match(line))
    ]
    if not results:
        raise RuntimeError("No se pudieron leer las filas de resultados de e4.cpp.")
    return results


def format_scientific(value: float) -> str:
    return f"{value:.2e}"


def build_figure(results: list[Result], selected_size: int) -> go.Figure:
    sizes = [row[0] for row in results]
    heuristic_ms = [row[2] for row in results]
    routes = [row[4] for row in results]
    brute_force_years = [row[5] for row in results]
    ratios = [row[6] for row in results]
    hover_data = [
        [row[1], row[3], row[4], row[5], row[6]] for row in results
    ]

    figure = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.11,
        row_heights=[0.25, 0.34, 0.41],
        subplot_titles=(
            "NN + 2-opt: tiempo medido",
            "Fuerza bruta: número de ciclos posibles",
            "Fuerza bruta: tiempo total estimado",
        ),
    )
    common_hover = (
        "n = %{x}<br>NN + 2-opt: %{customdata[0]:.4f} ms<br>"
        "Segundos por ruta: %{customdata[1]:.2e}<br>"
        "Rutas: %{customdata[2]:.2e}<br>"
        "Fuerza bruta: %{customdata[3]:.2e} años<br>"
        "Relación BF/heurística: %{customdata[4]:.2e}<extra></extra>"
    )
    color = ["#d45b45" if size == selected_size else "#197c78" for size in sizes]
    for row_number, values, name in (
        (1, heuristic_ms, "Tiempo NN + 2-opt (ms)"),
        (2, routes, "Rutas (n-1)!/2"),
        (3, brute_force_years, "Tiempo estimado (años)"),
    ):
        figure.add_trace(
            go.Scatter(
                x=sizes,
                y=values,
                mode="lines+markers",
                name=name,
                line={"color": "#197c78", "width": 2.2},
                marker={"size": 11, "color": color, "line": {"color": "#263238", "width": 1}},
                customdata=hover_data,
                hovertemplate=common_hover,
                showlegend=False,
            ),
            row=row_number,
            col=1,
        )
    figure.add_hline(
        y=AGE_OF_UNIVERSE_YEARS,
        line={"color": "#d45b45", "width": 1.5, "dash": "dash"},
        annotation_text="Edad del universo (aprox.)",
        annotation_position="top left",
        annotation_font={"size": 10, "color": "#d45b45"},
        row=3,
        col=1,
    )
    figure.update_yaxes(type="log", row=1, col=1, title_text="Milisegundos", gridcolor="#d9dfdc")
    figure.update_yaxes(type="log", row=2, col=1, title_text="Cantidad de rutas", gridcolor="#d9dfdc")
    figure.update_yaxes(type="log", row=3, col=1, title_text="Años (escala logarítmica)", gridcolor="#d9dfdc")
    figure.update_xaxes(type="linear", tickmode="array", tickvals=sizes, gridcolor="#e1e4df")
    figure.update_xaxes(title_text="Número de ciudades (n)", row=3, col=1)
    figure.update_layout(
        template="plotly_white",
        height=800,
        margin={"l": 75, "r": 25, "t": 65, "b": 52},
        paper_bgcolor="#f7f6f0",
        plot_bgcolor="#f7f6f0",
        clickmode="event+select",
        uirevision="e4-growth",
    )
    for annotation in figure.layout.annotations:
        annotation.font = {"size": 11, "color": "#465458"}
    return figure


def create_png(results: list[Result], output: Path) -> None:
    sizes = [row[0] for row in results]
    heuristic_ms = [row[2] for row in results]
    routes = [row[4] for row in results]
    brute_force_years = [row[5] for row in results]
    ratios = [row[6] for row in results]

    figure, axes = plt.subplots(
        3,
        1,
        figsize=(10.5, 9.5),
        sharex=True,
        gridspec_kw={"height_ratios": [1, 1.15, 1.4]},
    )
    figure.patch.set_facecolor("#f7f6f0")
    for axis in axes:
        axis.set_facecolor("#f7f6f0")
        axis.set_yscale("log")
        axis.grid(color="#d9dfdc", linewidth=0.7, which="both")
        axis.set_axisbelow(True)
        axis.spines[["top", "right"]].set_visible(False)

    axes[0].plot(sizes, heuristic_ms, color="#197c78", marker="o", linewidth=2.2, markersize=7)
    axes[0].scatter(sizes, heuristic_ms, color="#197c78", edgecolor="#263238", zorder=3)
    for size, value in zip(sizes, heuristic_ms):
        axes[0].annotate(f"{value:.4f} ms", (size, value), xytext=(0, 9), textcoords="offset points", ha="center", fontsize=8)
    axes[0].set_ylabel("Tiempo medido (ms)")
    axes[0].set_title("e4 · Escalabilidad: NN + 2-opt frente a fuerza bruta", loc="left", fontsize=14, fontweight="bold", pad=12)

    axes[1].plot(sizes, routes, color="#327b87", marker="o", linewidth=2.2, markersize=7)
    axes[1].scatter(sizes, routes, color="#327b87", edgecolor="#263238", zorder=3)
    for size, value in zip(sizes, routes):
        axes[1].annotate(format_scientific(value), (size, value), xytext=(0, 9), textcoords="offset points", ha="center", fontsize=8)
    axes[1].set_ylabel("Rutas posibles")

    axes[2].plot(sizes, brute_force_years, color="#d45b45", marker="o", linewidth=2.2, markersize=7)
    axes[2].scatter(sizes, brute_force_years, color="#d45b45", edgecolor="#263238", zorder=3)
    for size, value, ratio in zip(sizes, brute_force_years, ratios):
        is_smallest = size == min(sizes)
        axes[2].annotate(
            f"{value:.0f} años" if is_smallest else f"{format_scientific(value)} años\nBF/heur. {format_scientific(ratio)}×",
            (size, value),
            xytext=(32, -12) if is_smallest else (0, 9),
            textcoords="offset points",
            ha="left" if is_smallest else "center",
            va="top" if is_smallest else "bottom",
            fontsize=8,
        )
    axes[2].axhline(
        AGE_OF_UNIVERSE_YEARS,
        color="#263238",
        linewidth=1.2,
        linestyle=(0, (4, 3)),
        label="Edad del universo ≈ 1.38×10¹⁰ años",
    )
    axes[2].set_ylim(min(brute_force_years) / 100, max(brute_force_years) * 10)
    axes[2].set_ylabel("Estimación (años)")
    axes[2].set_xlabel("Número de ciudades (n)")
    axes[2].set_xticks(sizes)
    axes[2].legend(frameon=False, loc="upper left", fontsize=8)
    figure.text(
        0.99,
        0.012,
        "Fuerza bruta: estimación; no se ejecutó la búsqueda exhaustiva.",
        ha="right",
        fontsize=8,
        color="#647276",
    )
    figure.tight_layout(rect=(0, 0.035, 1, 1), h_pad=1.3)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(figure)
    print(f"Imagen guardada en: {output.resolve()}")


def create_app(results: list[Result]) -> Dash:
    selected_size = results[-1][0]
    row = next(item for item in results if item[0] == selected_size)
    app = Dash(__name__)
    app.title = "TSP e4 | Escalabilidad"
    app.layout = html.Main(
        [
            html.Header(
                [
                    html.P("TSP / EXPERIMENTO 04", className="eyebrow"),
                    html.H1("El costo de crecer"),
                    html.P("Tiempo medido para NN + 2-opt frente a una estimación de fuerza bruta."),
                ],
                className="header",
            ),
            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H2("Escalabilidad del TSP"),
                                    html.Span("Haz clic en un punto para inspeccionar ese tamaño", className="graph-meta"),
                                ],
                                className="graph-heading",
                            ),
                            dcc.Graph(
                                id="growth-chart",
                                figure=build_figure(results, selected_size),
                                config={"displayModeBar": False, "responsive": True},
                                clickData={"points": [{"x": selected_size}]},
                            ),
                        ],
                        className="chart-panel",
                    ),
                    html.Aside(
                        [
                            html.P("TAMAÑO SELECCIONADO", className="eyebrow"),
                            html.Div(f"n = {selected_size}", id="selected-size", className="selected-size"),
                            html.Div(
                                [html.Span("Costo de NN + 2-opt", className="metric-label"), html.Strong("", id="heuristic-cost", className="metric-value")],
                                className="metric-row",
                            ),
                            html.Div(
                                [html.Span("Tiempo heurístico", className="metric-label"), html.Strong("", id="heuristic-time", className="metric-value")],
                                className="metric-row",
                            ),
                            html.Div(
                                [html.Span("Rutas para fuerza bruta", className="metric-label"), html.Strong("", id="route-count", className="metric-value")],
                                className="metric-row",
                            ),
                            html.Div(
                                [html.Span("Fuerza bruta estimada", className="metric-label"), html.Strong("", id="brute-years", className="metric-value")],
                                className="metric-row",
                            ),
                            html.Div(
                                [html.Span("BF / heurística", className="metric-label"), html.Strong("", id="time-ratio", className="metric-value")],
                                className="metric-row",
                            ),
                            html.P(id="comparison-note", className="note"),
                            html.P("La fuerza bruta no se ejecuta: el tiempo se estima multiplicando el tiempo medido por ruta por la cantidad de ciclos posibles.", className="caution"),
                        ],
                        className="summary-panel",
                    ),
                ],
                className="workspace",
            ),
            html.Footer("Eje vertical logarítmico · la línea de referencia indica la edad aproximada del universo", className="footer"),
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
      .selected-size { margin: 18px 0 12px; font: 500 25px 'DM Mono', monospace; }
      .metric-row { display: flex; justify-content: space-between; gap: 8px; align-items: baseline; border-top: 1px solid var(--line); padding: 12px 0 10px; }
      .metric-label { color: var(--muted); font-size: 11px; }
      .metric-value { max-width: 58%; font: 500 11px 'DM Mono', monospace; text-align: right; overflow-wrap: anywhere; }
      .note, .caution { margin: 14px 0 12px; color: var(--muted); font-size: 11px; line-height: 1.55; }
      .caution { border-left: 2px solid #d45b45; padding-left: 10px; }
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
        Output("selected-size", "children"),
        Output("heuristic-cost", "children"),
        Output("heuristic-time", "children"),
        Output("route-count", "children"),
        Output("brute-years", "children"),
        Output("time-ratio", "children"),
        Output("comparison-note", "children"),
        Output("growth-chart", "figure"),
        Input("growth-chart", "clickData"),
    )
    def select_size(click_data: dict[str, object] | None) -> tuple[str, str, str, str, str, str, str, go.Figure]:
        size = selected_size
        if click_data and click_data.get("points"):
            try:
                size = int(click_data["points"][0]["x"])
            except (TypeError, ValueError):
                pass
        selected = next(item for item in results if item[0] == size)
        _, cost, heuristic_ms, seconds_per_route, route_count, years, ratio = selected
        universe_ratio = years / AGE_OF_UNIVERSE_YEARS
        note = (
            f"La estimación equivale a {universe_ratio:.2e} edades del universo."
            if universe_ratio >= 1
            else f"La estimación equivale a {universe_ratio:.2e} edades del universo."
        )
        return (
            f"n = {size}",
            f"{cost:.3f}",
            f"{heuristic_ms:.4f} ms",
            format_scientific(route_count),
            f"{format_scientific(years)} años",
            f"{format_scientific(ratio)}×",
            note,
            build_figure(results, size),
        )

    return app


def main() -> None:
    results = load_cpp_results()
    create_png(results, HERE / "e4_escalabilidad_tsp.png")
    app = create_app(results)
    for size, cost, heuristic_ms, _, route_count, years, ratio in results:
        print(
            f"n={size}: costo={cost:.3f}, heurística={heuristic_ms:.4f} ms, "
            f"rutas={format_scientific(route_count)}, fuerza bruta={format_scientific(years)} años, "
            f"relación={format_scientific(ratio)}x"
        )
    app.run(debug=False, port=8055)


if __name__ == "__main__":
    main()
