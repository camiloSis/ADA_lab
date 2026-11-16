from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, ctx, dcc, html
from matplotlib.patches import FancyArrowPatch


DISTANCES = (
    (0, 10, 15, 20, 25),
    (10, 0, 35, 25, 30),
    (15, 35, 0, 30, 5),
    (20, 25, 30, 0, 15),
    (25, 30, 5, 15, 0),
)
INITIAL_ROUTE = [0, 1, 2, 4, 3]
CITY_COUNT = len(DISTANCES)
POINTS = {
    city: (
        math.cos(math.pi / 2 + 2 * math.pi * city / CITY_COUNT),
        math.sin(math.pi / 2 + 2 * math.pi * city / CITY_COUNT),
    )
    for city in range(CITY_COUNT)
}


def route_cost(route: list[int]) -> int:
    cycle = route + [route[0]]
    return sum(DISTANCES[first][second] for first, second in zip(cycle, cycle[1:]))


def reverse_segment(route: list[int], first: int, last: int) -> list[int]:
    return route[:first] + list(reversed(route[first : last + 1])) + route[last + 1 :]


def build_history() -> list[dict[str, object]]:
    route = INITIAL_ROUTE.copy()
    history: list[dict[str, object]] = []
    pass_number = 0

    while True:
        pass_number += 1
        improved = False
        for first in range(1, CITY_COUNT - 1):
            for last in range(first + 1, CITY_COUNT):
                before = route.copy()
                proposal = reverse_segment(route, first, last)
                before_cost = route_cost(route)
                proposal_cost = route_cost(proposal)
                accepted = proposal_cost < before_cost
                if accepted:
                    route = proposal
                    improved = True
                history.append(
                    {
                        "pass": pass_number,
                        "first": first,
                        "last": last,
                        "before": before,
                        "proposal": proposal,
                        "route": route.copy(),
                        "before_cost": before_cost,
                        "proposal_cost": proposal_cost,
                        "accepted": accepted,
                    }
                )
        if not improved:
            break

    return history


HISTORY = build_history()
FINAL_ROUTE = list(HISTORY[-1]["route"])


def edge_set(route: list[int]) -> set[tuple[int, int]]:
    cycle = route + [route[0]]
    return {tuple(sorted((first, second))) for first, second in zip(cycle, cycle[1:])}


def build_figure(step: int) -> go.Figure:
    figure = go.Figure()
    event = HISTORY[step - 1] if step > 0 else None
    route = list(event["route"]) if event else INITIAL_ROUTE.copy()
    current_edges = edge_set(route)
    candidate_edges = edge_set(list(event["proposal"])) if event else set()
    changed_edges = candidate_edges - current_edges
    if event and not event["accepted"]:
        changed_edges = candidate_edges - edge_set(list(event["before"]))

    for first in range(CITY_COUNT):
        for second in range(first + 1, CITY_COUNT):
            edge = (first, second)
            in_route = edge in current_edges
            is_candidate = edge in changed_edges
            color = "#d45b45" if in_route else "#cf9b2e" if is_candidate else "#a4adae"
            width = 3.6 if in_route else 2.5 if is_candidate else 1.1
            dash = "solid" if in_route else "dash" if is_candidate else "solid"
            figure.add_trace(
                go.Scatter(
                    x=[POINTS[first][0], POINTS[second][0]],
                    y=[POINTS[first][1], POINTS[second][1]],
                    mode="lines",
                    line={"color": color, "width": width, "dash": dash},
                    opacity=1 if in_route or is_candidate else 0.55,
                    hoverinfo="skip",
                    showlegend=False,
                )
            )
            midpoint = (
                (POINTS[first][0] + POINTS[second][0]) / 2,
                (POINTS[first][1] + POINTS[second][1]) / 2,
            )
            figure.add_annotation(
                x=midpoint[0],
                y=midpoint[1],
                text=str(DISTANCES[first][second]),
                showarrow=False,
                yshift=9,
                font={"size": 11, "color": "#9c3d31" if in_route else "#916a1d" if is_candidate else "#465458"},
                bgcolor="rgba(255,255,255,0.9)",
                borderpad=2,
            )

    for first, second in zip(route, route[1:] + route[:1]):
        figure.add_annotation(
            x=POINTS[second][0],
            y=POINTS[second][1],
            ax=POINTS[first][0],
            ay=POINTS[first][1],
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            showarrow=True,
            arrowhead=3,
            arrowsize=1.2,
            arrowwidth=2.2,
            arrowcolor="#d45b45",
            startstandoff=20,
            standoff=20,
        )

    figure.add_trace(
        go.Scatter(
            x=[POINTS[city][0] for city in range(CITY_COUNT)],
            y=[POINTS[city][1] for city in range(CITY_COUNT)],
            mode="markers+text",
            text=[str(city) for city in range(CITY_COUNT)],
            textposition="middle center",
            textfont={"size": 16, "color": "#17252a"},
            marker={"size": 48, "color": "#f0c44f", "line": {"color": "#263238", "width": 1.5}},
            hovertemplate="Ciudad %{text}<extra></extra>",
            showlegend=False,
        )
    )
    figure.update_layout(
        template="plotly_white",
        height=570,
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        xaxis={"visible": False, "range": [-1.4, 1.4], "fixedrange": True, "scaleanchor": "y"},
        yaxis={"visible": False, "range": [-1.35, 1.35], "fixedrange": True},
        paper_bgcolor="#f7f6f0",
        plot_bgcolor="#f7f6f0",
        uirevision="tsp-2opt",
    )
    return figure


def describe_step(step: int) -> str:
    if step == 0:
        return "Ruta inicial del programa C++; todavía no se han probado intercambios."
    event = HISTORY[step - 1]
    result = "aceptada" if event["accepted"] else "rechazada"
    return (
        f"Barrido {event['pass']}: invertir posiciones {event['first']}–{event['last']} "
        f"({event['before_cost']} → {event['proposal_cost']}). Mejora {result}."
    )


def draw_static_graph(axis: plt.Axes, route: list[int]) -> None:
    selected_edges = edge_set(route)
    for first in range(CITY_COUNT):
        for second in range(first + 1, CITY_COUNT):
            selected = (first, second) in selected_edges
            axis.plot(
                (POINTS[first][0], POINTS[second][0]),
                (POINTS[first][1], POINTS[second][1]),
                color="#d45b45" if selected else "#a4adae",
                linewidth=2.5 if selected else 0.9,
                alpha=0.95 if selected else 0.55,
                zorder=1,
            )
            midpoint = (
                (POINTS[first][0] + POINTS[second][0]) / 2,
                (POINTS[first][1] + POINTS[second][1]) / 2,
            )
            axis.annotate(
                str(DISTANCES[first][second]),
                midpoint,
                xytext=(0, 5),
                textcoords="offset points",
                ha="center",
                va="center",
                fontsize=8,
                color="#9c3d31" if selected else "#465458",
                bbox={"boxstyle": "round,pad=0.15", "facecolor": "white", "edgecolor": "none", "alpha": 0.88},
                zorder=3,
            )
    cycle = route + [route[0]]
    for first, second in zip(cycle, cycle[1:]):
        axis.add_patch(
            FancyArrowPatch(
                POINTS[first],
                POINTS[second],
                arrowstyle="-|>",
                mutation_scale=13,
                linewidth=2,
                color="#d45b45",
                shrinkA=18,
                shrinkB=18,
                zorder=2,
            )
        )
    axis.scatter(
        [POINTS[city][0] for city in range(CITY_COUNT)],
        [POINTS[city][1] for city in range(CITY_COUNT)],
        s=520,
        color="#f0c44f",
        edgecolor="#263238",
        linewidth=1.2,
        zorder=4,
    )
    for city, (x, y) in POINTS.items():
        axis.text(x, y, str(city), ha="center", va="center", fontsize=12, fontweight="bold", zorder=5)
    axis.set_aspect("equal")
    axis.set_xlim(-1.45, 1.45)
    axis.set_ylim(-1.4, 1.45)
    axis.axis("off")


def create_static_image(output: Path) -> None:
    figure, (initial_axis, result_axis) = plt.subplots(1, 2, figsize=(12, 6))
    figure.suptitle("TSP: mejora local 2-opt", fontsize=16, fontweight="bold")
    initial_axis.set_title(f"Ruta inicial · costo {route_cost(INITIAL_ROUTE)}", fontsize=11, pad=14)
    result_axis.set_title(f"Ruta final · costo {route_cost(FINAL_ROUTE)}", fontsize=11, pad=14)
    draw_static_graph(initial_axis, INITIAL_ROUTE)
    draw_static_graph(result_axis, FINAL_ROUTE)
    figure.text(
        0.5,
        0.045,
        "Inicial: 0 → 1 → 2 → 4 → 3 → 0     |     2-opt: 0 → 1 → 3 → 4 → 2 → 0",
        ha="center",
        fontsize=10,
        color="#263238",
    )
    figure.subplots_adjust(top=0.84, bottom=0.14, wspace=0.12)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(figure)
    print(f"Imagen guardada en: {output.resolve()}")
    print(f"Ruta inicial: {' -> '.join(map(str, INITIAL_ROUTE + [INITIAL_ROUTE[0]]))} (costo {route_cost(INITIAL_ROUTE)})")
    print(f"Ruta 2-opt: {' -> '.join(map(str, FINAL_ROUTE + [FINAL_ROUTE[0]]))} (costo {route_cost(FINAL_ROUTE)})")


app = Dash(__name__)
app.title = "TSP | 2-opt"
app.layout = html.Main(
    [
        html.Header(
            [
                html.P("ALGORITMOS Y ESTRUCTURAS", className="eyebrow"),
                html.H1("TSP / Mejora local 2-opt"),
                html.P("Sigue cada inversión de segmento y observa si reduce el costo del ciclo."),
            ],
            className="header",
        ),
        html.Section(
            [
                html.Div(
                    [
                        html.Div(
                            [html.H2("Grafo ponderado"), html.Span("5 ciudades · ciclo dirigido", className="graph-meta")],
                            className="graph-heading",
                        ),
                        dcc.Graph(id="tsp-graph", figure=build_figure(0), config={"displayModeBar": False, "responsive": True}),
                    ],
                    className="graph-panel",
                ),
                html.Aside(
                    [
                        html.P("RECORRIDO ACTUAL", className="eyebrow"),
                        html.Div("0 → 1 → 2 → 4 → 3 → 0", id="route-display", className="route-display"),
                        html.Div(describe_step(0), id="step-description", className="step-description"),
                        html.Div(
                            [html.Span("Evaluación", className="metric-label"), html.Strong(f"0 / {len(HISTORY)}", id="step-count", className="metric-value")],
                            className="step-metric",
                        ),
                        dcc.Slider(
                            id="step-slider",
                            min=0,
                            max=len(HISTORY),
                            step=1,
                            value=0,
                            marks={0: "Inicio", len(HISTORY): "Final"},
                            included=True,
                            tooltip={"placement": "bottom", "always_visible": False},
                        ),
                        html.Div(
                            [
                                html.Button("←", id="back-button", n_clicks=0, title="Evaluación anterior", className="icon-button"),
                                html.Button("▶ Reproducir", id="play-button", n_clicks=0, className="play-button"),
                                html.Button("→", id="next-button", n_clicks=0, title="Siguiente evaluación", className="icon-button"),
                            ],
                            className="controls",
                        ),
                        dcc.Interval(id="play-interval", interval=950, n_intervals=0, disabled=True),
                        html.Div(
                            [html.Span("Costo del ciclo", className="metric-label"), html.Strong(str(route_cost(INITIAL_ROUTE)), id="cost-value", className="metric-value")],
                            className="cost-metric",
                        ),
                        html.Div(
                            [html.Span("Rojo", className="legend-current"), html.Span("Dorado discontinuo", className="legend-proposal")],
                            className="legend",
                        ),
                        html.P("El dorado muestra las aristas nuevas de la propuesta; el rojo, el ciclo vigente.", className="note"),
                    ],
                    className="control-panel",
                ),
            ],
            className="workspace",
        ),
        html.Footer("2-opt: invierte segmentos y conserva solo mejoras estrictas", className="footer"),
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
      .workspace { display: grid; grid-template-columns: minmax(0, 1fr) 330px; gap: 34px; align-items: start; padding-top: 24px; }
      .graph-panel { min-width: 0; }
      .graph-heading { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; padding: 0 8px; }
      h2 { margin: 0; font-size: 16px; }
      .graph-meta { color: var(--muted); font: 11px 'DM Mono', monospace; }
      .control-panel { border-left: 1px solid var(--line); padding: 10px 0 8px 26px; min-height: 500px; }
      .route-display { min-height: 66px; padding: 8px 0; font: 500 15px 'DM Mono', monospace; line-height: 1.8; overflow-wrap: anywhere; }
      .step-description { min-height: 78px; color: var(--muted); font-size: 13px; line-height: 1.55; }
      .step-metric, .cost-metric { display: flex; justify-content: space-between; align-items: baseline; border-top: 1px solid var(--line); padding: 15px 0 12px; }
      .metric-label { color: var(--muted); font-size: 12px; }
      .metric-value { font: 500 13px 'DM Mono', monospace; }
      #step-slider { margin: 0 4px 26px; width: calc(100% - 8px); }
      .controls { display: grid; grid-template-columns: 42px 1fr 42px; gap: 8px; margin-bottom: 22px; }
      button { height: 42px; border: 1px solid var(--line); border-radius: 4px; background: transparent; color: var(--ink); font: 600 14px 'Manrope', sans-serif; cursor: pointer; }
      button:hover { border-color: var(--ink); }
      .play-button { background: var(--ink); color: white; border-color: var(--ink); }
      .play-button:hover { background: #34474c; color: white; }
      .legend { display: flex; flex-wrap: wrap; gap: 14px; border-top: 1px solid var(--line); padding-top: 14px; color: var(--muted); font-size: 11px; }
      .legend-current::before, .legend-proposal::before { content: ''; display: inline-block; width: 18px; margin: 0 6px 3px 0; border-top: 3px solid #d45b45; }
      .legend-proposal::before { border-top: 2px dashed #cf9b2e; }
      .note { margin-top: 14px; color: var(--muted); font-size: 11px; line-height: 1.6; }
      .footer { margin-top: 20px; border-top: 1px solid var(--line); padding-top: 15px; color: var(--muted); font: 10px 'DM Mono', monospace; }
      @media (max-width: 760px) {
        .page { padding: 24px 18px 20px; }
        h1 { font-size: 25px; }
        .workspace { grid-template-columns: 1fr; gap: 12px; }
        .control-panel { border-left: 0; border-top: 1px solid var(--line); padding: 22px 4px 4px; min-height: 0; }
        #tsp-graph { height: 390px !important; }
      }
    </style>
  </head>
  <body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer></body>
</html>"""


@app.callback(
    Output("step-slider", "value"),
    Output("play-interval", "disabled"),
    Output("play-button", "children"),
    Input("back-button", "n_clicks"),
    Input("next-button", "n_clicks"),
    Input("play-button", "n_clicks"),
    Input("play-interval", "n_intervals"),
    Input("step-slider", "value"),
    State("play-interval", "disabled"),
    State("step-slider", "value"),
)
def control_step(
    _back_clicks: int,
    _next_clicks: int,
    _play_clicks: int,
    _interval_count: int,
    slider_value: int,
    interval_disabled: bool,
    current_step: int,
) -> tuple[int, bool, str]:
    trigger = ctx.triggered_id
    step = current_step
    playing = not interval_disabled

    if trigger == "back-button":
        step = max(0, current_step - 1)
        playing = False
    elif trigger == "next-button":
        step = min(len(HISTORY), current_step + 1)
        playing = False
    elif trigger == "play-button":
        if playing:
            playing = False
        elif current_step >= len(HISTORY):
            step = 0
            playing = True
        else:
            playing = True
    elif trigger == "play-interval":
        step = min(len(HISTORY), current_step + 1)
        if step >= len(HISTORY):
            playing = False
    elif trigger == "step-slider":
        step = slider_value
        playing = False

    return step, not playing, "❚❚ Pausar" if playing else "▶ Reproducir"


@app.callback(
    Output("tsp-graph", "figure"),
    Output("route-display", "children"),
    Output("step-description", "children"),
    Output("step-count", "children"),
    Output("cost-value", "children"),
    Input("step-slider", "value"),
)
def update_visualization(step: int) -> tuple[go.Figure, str, str, str, str]:
    event = HISTORY[step - 1] if step > 0 else None
    route = list(event["route"]) if event else INITIAL_ROUTE.copy()
    route_text = " → ".join(map(str, route + [route[0]]))
    if event:
        before_cost = int(event["before_cost"])
        proposal_cost = int(event["proposal_cost"])
        accepted = "aceptada" if event["accepted"] else "rechazada"
        cost_text = f"{route_cost(route)} · propuesta {proposal_cost} ({accepted})"
        detail = (
            f"{describe_step(step)} Costos evaluados: {before_cost} → {proposal_cost}."
        )
    else:
        cost_text = str(route_cost(route))
        detail = describe_step(step)
    return build_figure(step), route_text, detail, f"{step} / {len(HISTORY)}", cost_text


if __name__ == "__main__":
    image_path = Path(__file__).with_name("grafo_tsp_2opt.png")
    create_static_image(image_path)
    app.run(debug=False, port=8051)
