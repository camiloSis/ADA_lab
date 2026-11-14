from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.widgets import CheckButtons

from visualizar_ruta import (
    best_heuristic_route,
    distance_matrix,
    exact_route,
    load_locations,
    route_cost,
)


def project_coordinates(locations: list[tuple[str, float, float]]) -> list[tuple[float, float]]:
    mean_latitude = sum(latitude for _, latitude, _ in locations) / len(locations)
    mean_longitude = sum(longitude for _, _, longitude in locations) / len(locations)
    longitude_scale = math.cos(math.radians(mean_latitude))
    return [
        ((longitude - mean_longitude) * longitude_scale, latitude - mean_latitude)
        for _, latitude, longitude in locations
    ]


def draw_nodes(axis: plt.Axes, locations: list[tuple[str, float, float]], points: list[tuple[float, float]]) -> None:
    axis.scatter(
        [point[0] for point in points],
        [point[1] for point in points],
        s=42,
        color="#f0c44f",
        edgecolor="#263238",
        linewidth=0.8,
        zorder=3,
    )
    central_nodes = [
        index for index, (x, y) in enumerate(points) if math.hypot(x, y) < 0.02
    ]
    central_positions = {
        index: position for position, index in enumerate(central_nodes)
    }
    for index, (x, y) in enumerate(points):
        if index in central_positions:
            angle = 2 * math.pi * central_positions[index] / len(central_nodes)
            offset = (55 * math.cos(angle), 55 * math.sin(angle))
            arrow = {"arrowstyle": "-", "color": "#7b858a", "lw": 0.6}
        else:
            angle = math.atan2(y, x)
            offset = (12 * math.cos(angle), 12 * math.sin(angle))
            arrow = None
        axis.annotate(
            str(index),
            (x, y),
            xytext=offset,
            textcoords="offset points",
            ha="center",
            va="center",
            fontsize=7,
            color="#17252a",
            bbox={"boxstyle": "round,pad=0.15", "facecolor": "white", "edgecolor": "none", "alpha": 0.8},
            arrowprops=arrow,
            zorder=4,
        )
    axis.set_aspect("equal", adjustable="datalim")
    axis.set_xlabel("Longitud (escala local)")
    axis.set_ylabel("Latitud")
    axis.grid(color="#d9e0e3", linewidth=0.6, alpha=0.8)


def create_figure(output: Path, show: bool) -> None:
    locations = load_locations()
    distances = distance_matrix(locations)
    points = project_coordinates(locations)
    heuristic = best_heuristic_route(distances)
    optimal = exact_route(distances)
    original = list(range(len(locations)))

    figure, (initial_axis, result_axis) = plt.subplots(1, 2, figsize=(13, 7))
    figure.subplots_adjust(left=0.07, right=0.78, bottom=0.25, top=0.86, wspace=0.22)
    figure.suptitle("TSP de lugares emblemáticos de Arequipa", fontsize=14, fontweight="bold")
    initial_axis.set_title("Estado inicial: grafo completo")
    result_axis.set_title("Rutas calculadas")

    graph_edges = [
        [points[first], points[second]]
        for first in range(len(points))
        for second in range(first + 1, len(points))
    ]
    initial_axis.add_collection(
        LineCollection(graph_edges, colors="#9aa7ad", linewidths=0.65, alpha=0.55, zorder=1)
    )
    draw_nodes(initial_axis, locations, points)
    draw_nodes(result_axis, locations, points)

    def draw_route(axis: plt.Axes, route: list[int], color: str, **style: object) -> plt.Line2D:
        cycle = route + [route[0]]
        return axis.plot(
            [points[index][0] for index in cycle],
            [points[index][1] for index in cycle],
            color=color,
            zorder=2,
            **style,
        )[0]

    original_line = draw_route(result_axis, original, "#e98b32", linewidth=1.5, alpha=0.85)
    heuristic_line = draw_route(
        result_axis, heuristic, "#167d9a", linewidth=2.2, linestyle="--", alpha=0.9
    )
    optimal_line = draw_route(result_axis, optimal, "#c73535", linewidth=2.6, alpha=0.95)
    original_line.set_visible(False)

    for axis in (initial_axis, result_axis):
        axis.margins(0.13)

    checks_axis = figure.add_axes((0.81, 0.57, 0.17, 0.22))
    controls = CheckButtons(
        checks_axis,
        ("Orden original", "NN + 2-opt", "Óptimo exacto"),
        (False, False, True),
    )
    controls.labels[0].set_fontsize(9)
    controls.labels[1].set_fontsize(9)
    controls.labels[2].set_fontsize(9)

    lines = (original_line, heuristic_line, optimal_line)

    def toggle_route(label: str) -> None:
        index = ("Orden original", "NN + 2-opt", "Óptimo exacto").index(label)
        lines[index].set_visible(not lines[index].get_visible())
        figure.canvas.draw_idle()

    controls.on_clicked(toggle_route)
    figure.text(
        0.81,
        0.43,
        f"NN + 2-opt: {route_cost(heuristic, distances):.3f} km\n"
        f"Óptimo exacto: {route_cost(optimal, distances):.3f} km",
        fontsize=9,
        va="top",
    )

    left_mapping = "\n".join(
        f"{index}: {locations[index][0]}" for index in range((len(locations) + 1) // 2)
    )
    right_mapping = "\n".join(
        f"{index}: {locations[index][0]}"
        for index in range((len(locations) + 1) // 2, len(locations))
    )
    figure.text(0.07, 0.17, left_mapping, fontsize=7, va="top")
    figure.text(0.42, 0.17, right_mapping, fontsize=7, va="top")
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180, bbox_inches="tight")
    print(f"Imagen guardada en: {output.resolve()}")
    print(f"NN + 2-opt: {route_cost(heuristic, distances):.3f} km")
    print(f"Óptimo exacto (Held-Karp): {route_cost(optimal, distances):.3f} km")
    print("Ruta exacta: " + " -> ".join(locations[index][0] for index in optimal + [optimal[0]]))
    if show:
        plt.show()
    else:
        plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Grafica el grafo inicial y las rutas TSP de e5.cpp."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path(__file__).with_name("grafo_arequipa.png"),
        help="imagen PNG de salida (por defecto: grafo_arequipa.png junto al script)",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="guardar la imagen sin abrir la ventana interactiva",
    )
    arguments = parser.parse_args()
    create_figure(arguments.output, show=not arguments.no_show)


if __name__ == "__main__":
    main()