from __future__ import annotations

import math

import plotly.graph_objects as go
from dash import Dash, Input, Output, State, dcc, html, ctx


DISTANCES = (
    (0, 10, 15, 20, 25),
    (10, 0, 35, 25, 30),
    (15, 35, 0, 30, 5),
    (20, 25, 30, 0, 15),
    (25, 30, 5, 15, 0),
)
CITY_COUNT = len(DISTANCES)
POINTS = {
    city: (
        math.cos(math.pi / 2 + 2 * math.pi * city / CITY_COUNT),
        math.sin(math.pi / 2 + 2 * math.pi * city / CITY_COUNT),
    )
    for city in range(CITY_COUNT)
}


def next_city(route: list[int]) -> int:
    current = route[-1]
    unvisited = (city for city in range(CITY_COUNT) if city not in route)
    return min(unvisited, key=lambda city: DISTANCES[current][city])


def route_cost(route: list[int]) -> int:
    cycle = route + [route[0]]
    return sum(DISTANCES[first][second] for first, second in zip(cycle, cycle[1:]))


def build_figure(route: list[int]) -> go.Figure:
    figure = go.Figure()
    selected_edges = set(zip(route, route[1:]))
    completed = len(route) == CITY_COUNT
    if completed:
        selected_edges.add((route[-1], route[0]))

    for first in range(CITY_COUNT):
        for second in range(first + 1, CITY_COUNT):
            selected = (first, second) in selected_edges or (second, first) in selected_edges
            color = "#d45b45" if selected else "#9aa5a8"
            width = 3.5 if selected else 1.2
            alpha = 1.0 if selected else 0.62
            figure.add_trace(
                go.Scatter(
                    x=[POINTS[first][0], POINTS[second][0]],
                    y=[POINTS[first][1], POINTS[second][1]],
                    mode="lines",
                    line={"color": color, "width": width},
                    opacity=alpha,
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
                font={"size": 12, "color": "#9c3d31" if selected else "#465458"},
                bgcolor="rgba(255,255,255,0.9)",
                borderpad=2,
            )

    for first, second in zip(route, route[1:]):
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
    if completed:
        figure.add_annotation(
            x=POINTS[route[0]][0],
            y=POINTS[route[0]][1],
            ax=POINTS[route[-1]][0],
            ay=POINTS[route[-1]][1],
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
            textfont={"size": 16, "color": "#17252a", "family": "sans-serif"},
            marker={"size": 48, "color": "#f0c44f", "line": {"color": "#263238", "width": 1.5}},
            customdata=[[city] for city in range(CITY_COUNT)],
            hovertemplate="Ciudad %{customdata[0]}<extra></extra>",
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
        uirevision="tsp-graph",
    )
    return figure


def step_description(route: list[int]) -> str:
    if len(route) == 1:
        return "Inicio: el recorrido parte de la ciudad 0."
    previous, current = route[-2:]
    distance = DISTANCES[previous][current]
    if len(route) == CITY_COUNT:
        return f"Paso {CITY_COUNT - 1}: desde {previous}, se elige {current} ({distance}), la más cercana sin visitar."
    return f"Paso {len(route) - 1}: desde {previous}, se elige {current} ({distance}), la más cercana sin visitar."


app = Dash(__name__)
app.title = "TSP | Vecino más cercano"

app.layout = html.Main(
    [
        html.Header(
            [
                html.P("Guia de implementacion del TSP."),
            ],
            className="header",
        ),
        html.Section(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2("Grafo de distancias"),
                                html.Span("5 ciudades · inicio en 0", className="graph-meta"),
                            ],
                            className="graph-heading",
                        ),
                        dcc.Graph(
                            id="tsp-graph",
                            figure=build_figure([0]),
                            config={"displayModeBar": False, "responsive": True},
                        ),
                    ],
                    className="graph-panel",
                ),
                html.Aside(
                    [
                        html.P("RECORRIDO", className="eyebrow"),
                        html.Div("0", id="route-display", className="route-display"),
                        html.Div(step_description([0]), id="step-description", className="step-description"),
                        html.Div(
                            [
                                html.Span("Paso", className="metric-label"),
                                html.Strong("0 / 4", id="step-count", className="metric-value"),
                            ],
                            className="step-metric",
                        ),
                        dcc.Slider(
                            id="step-slider",
                            min=0,
                            max=CITY_COUNT - 1,
                            step=1,
                            value=0,
                            marks={step: str(step) for step in range(CITY_COUNT)},
                            included=True,
                            tooltip={"placement": "bottom", "always_visible": False},
                        ),
                        html.Div(
                            [
                                html.Button("←", id="back-button", n_clicks=0, title="Paso anterior", className="icon-button"),
                                html.Button("▶ Reproducir", id="play-button", n_clicks=0, className="play-button"),
                                html.Button("→", id="next-button", n_clicks=0, title="Siguiente paso", className="icon-button"),
                            ],
                            className="controls",
                        ),
                        dcc.Interval(id="play-interval", interval=1100, n_intervals=0, disabled=True),
                        html.Div(
                            [
                                html.Span("Costo del ciclo", className="metric-label"),
                                html.Strong("--", id="cost-value", className="metric-value"),
                            ],
                            className="cost-metric",
                        ),
                        html.P(
                            "El retorno a la ciudad inicial se agrega al completar la última ciudad.",
                            className="note",
                        ),
                    ],
                    className="control-panel",
                ),
            ],
            className="workspace",
        ),
        html.Footer("Matriz de distancias simétrica · selección greedy local", className="footer"),
    ],
    className="page",
)

app.index_string = """<!DOCTYPE html>
<html>
  <head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
      :root { color-scheme: light; --ink: #17252a; --muted: #647276; --line: #d7ddda; --paper: #f7f6f0; --accent: #d45b45; --gold: #f0c44f; }
      * { box-sizing: border-box; }
      body { margin: 0; background: var(--paper); color: var(--ink); font-family: 'Manrope', sans-serif; }
      .page { max-width: 1280px; margin: 0 auto; padding: 38px 42px 24px; }
      .header { border-bottom: 1px solid var(--line); padding-bottom: 24px; }
      .eyebrow { margin: 0 0 9px; color: var(--accent); font: 500 11px 'DM Mono', monospace; }
      h1 { margin: 0; font-size: 32px; line-height: 1.15; font-weight: 800; }
      .header > p:last-child { margin: 8px 0 0; color: var(--muted); font-size: 14px; }
      .workspace { display: grid; grid-template-columns: minmax(0, 1fr) 310px; gap: 34px; align-items: start; padding-top: 24px; }
      .graph-panel { min-width: 0; }
      .graph-heading { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; padding: 0 8px; }
      h2 { margin: 0; font-size: 16px; }
      .graph-meta { color: var(--muted); font: 11px 'DM Mono', monospace; }
      .control-panel { border-left: 1px solid var(--line); padding: 10px 0 8px 26px; min-height: 500px; }
      .route-display { min-height: 60px; padding: 10px 0; font: 500 16px 'DM Mono', monospace; line-height: 1.8; overflow-wrap: anywhere; }
      .step-description { min-height: 62px; color: var(--muted); font-size: 13px; line-height: 1.55; }
      .step-metric, .cost-metric { display: flex; justify-content: space-between; align-items: baseline; border-top: 1px solid var(--line); padding: 16px 0 12px; }
      .metric-label { color: var(--muted); font-size: 12px; }
      .metric-value { font: 500 13px 'DM Mono', monospace; }
      #step-slider { margin: 0 4px 26px; width: calc(100% - 8px); }
      .controls { display: grid; grid-template-columns: 42px 1fr 42px; gap: 8px; margin-bottom: 24px; }
      button { height: 42px; border: 1px solid var(--line); border-radius: 4px; background: transparent; color: var(--ink); font: 600 14px 'Manrope', sans-serif; cursor: pointer; }
      button:hover { border-color: var(--ink); }
      .play-button { background: var(--ink); color: white; border-color: var(--ink); }
      .play-button:hover { background: #34474c; color: white; }
      .note { margin-top: 18px; color: var(--muted); font-size: 11px; line-height: 1.6; }
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
  <body>
    {%app_entry%}
    <footer>
      {%config%}
      {%scripts%}
      {%renderer%}
    </footer>
  </body>
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
        step = min(CITY_COUNT - 1, current_step + 1)
        playing = False
    elif trigger == "play-button":
        if playing:
            playing = False
        elif current_step >= CITY_COUNT - 1:
            step = 0
            playing = True
        else:
            playing = True
    elif trigger == "play-interval":
        if current_step >= CITY_COUNT - 1:
            playing = False
        else:
            step = current_step + 1
            if step >= CITY_COUNT - 1:
                playing = False
    elif trigger == "step-slider":
        step = slider_value
        playing = False

    label = "❚❚ Pausar" if playing else "▶ Reproducir"
    return step, not playing, label


@app.callback(
    Output("tsp-graph", "figure"),
    Output("route-display", "children"),
    Output("step-description", "children"),
    Output("step-count", "children"),
    Output("cost-value", "children"),
    Input("step-slider", "value"),
)
def update_visualization(step: int) -> tuple[go.Figure, str, str, str, str]:
    route = [0]
    for _ in range(step):
        route.append(next_city(route))
    route_text = " → ".join(str(city) for city in route)
    cost_text = str(route_cost(route)) if step == CITY_COUNT - 1 else "--"
    if step == CITY_COUNT - 1:
        route_text += " → 0"
    return (
        build_figure(route),
        route_text,
        step_description(route),
        f"{step} / {CITY_COUNT - 1}",
        cost_text,
    )


if __name__ == "__main__":
    app.run(debug=False)
