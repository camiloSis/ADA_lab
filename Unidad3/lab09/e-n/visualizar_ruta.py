from __future__ import annotations

import argparse
import math
import re
from array import array
from pathlib import Path

import folium


SOURCE = Path(__file__).with_name("e5.cpp")
EARTH_RADIUS_KM = 6371.0
EPSILON = 1e-9
LOCATION_PATTERN = re.compile(
    r'\{\s*"([^"]+)"\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\}'
)


def load_locations() -> list[tuple[str, float, float]]:
    source = SOURCE.read_text(encoding="utf-8")
    start = source.index("const vector<Lugar> LUGARES = {")
    end = source.index("\n};", start)
    locations = [
        (name, float(latitude), float(longitude))
        for name, latitude, longitude in LOCATION_PATTERN.findall(source[start:end])
    ]
    if len(locations) < 3:
        raise ValueError(f"Se encontraron solo {len(locations)} ubicaciones en {SOURCE.name}.")
    return locations


def haversine(first: tuple[float, float], second: tuple[float, float]) -> float:
    lat1, lon1 = map(math.radians, first)
    lat2, lon2 = map(math.radians, second)
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    value = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
    )
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(value))


def distance_matrix(locations: list[tuple[str, float, float]]) -> list[list[float]]:
    coordinates = [(latitude, longitude) for _, latitude, longitude in locations]
    return [
        [haversine(coordinates[first], coordinates[second]) for second in range(len(locations))]
        for first in range(len(locations))
    ]


def route_cost(route: list[int], distances: list[list[float]]) -> float:
    return sum(distances[city][route[(index + 1) % len(route)]] for index, city in enumerate(route))


def nearest_neighbor(start: int, distances: list[list[float]]) -> list[int]:
    route = [start]
    unvisited = set(range(len(distances))) - {start}
    while unvisited:
        current = route[-1]
        next_city = min(unvisited, key=lambda city: distances[current][city])
        route.append(next_city)
        unvisited.remove(next_city)
    return route


def two_opt(route: list[int], distances: list[list[float]]) -> list[int]:
    route = route.copy()
    count = len(route)
    improved = True
    while improved:
        improved = False
        for first_edge in range(count - 1):
            for second_edge in range(first_edge + 1, count):
                if first_edge == 0 and second_edge == count - 1:
                    continue
                first = route[first_edge]
                second = route[first_edge + 1]
                third = route[second_edge]
                fourth = route[(second_edge + 1) % count]
                delta = (
                    distances[first][third]
                    + distances[second][fourth]
                    - distances[first][second]
                    - distances[third][fourth]
                )
                if delta < -EPSILON:
                    route[first_edge + 1 : second_edge + 1] = reversed(
                        route[first_edge + 1 : second_edge + 1]
                    )
                    improved = True
    return route


def best_heuristic_route(distances: list[list[float]]) -> list[int]:
    candidates = [
        two_opt(nearest_neighbor(start, distances), distances)
        for start in range(len(distances))
    ]
    best_cost = min(route_cost(route, distances) for route in candidates)
    selected = next(
        route for route in candidates if route_cost(route, distances) - best_cost < EPSILON
    )
    start_index = selected.index(0)
    return selected[start_index:] + selected[:start_index]


def exact_route(distances: list[list[float]]) -> list[int]:
    city_count = len(distances)
    remaining_count = city_count - 1
    state_count = 1 << remaining_count
    cell_count = state_count * remaining_count
    costs = array("d", [math.inf]) * cell_count
    parents = array("b", [-1]) * cell_count

    for city in range(remaining_count):
        costs[(1 << city) * remaining_count + city] = distances[0][city + 1]

    for visited in range(1, state_count):
        remaining = visited
        while remaining:
            bit = remaining & -remaining
            last = bit.bit_length() - 1
            current_cost = costs[visited * remaining_count + last]
            if math.isfinite(current_cost):
                unvisited = (state_count - 1) ^ visited
                while unvisited:
                    next_bit = unvisited & -unvisited
                    next_city = next_bit.bit_length() - 1
                    next_state = visited | next_bit
                    next_index = next_state * remaining_count + next_city
                    candidate = current_cost + distances[last + 1][next_city + 1]
                    if candidate < costs[next_index]:
                        costs[next_index] = candidate
                        parents[next_index] = last
                    unvisited ^= next_bit
            remaining ^= bit

    full_state = state_count - 1
    last_city = min(
        range(remaining_count),
        key=lambda city: costs[full_state * remaining_count + city]
        + distances[city + 1][0],
    )

    reversed_path = []
    visited = full_state
    while visited:
        reversed_path.append(last_city + 1)
        parent = parents[visited * remaining_count + last_city]
        visited ^= 1 << last_city
        if visited:
            last_city = parent
    return [0, *reversed(reversed_path)]


def add_route_layer(
    map_view: folium.Map,
    name: str,
    route: list[int],
    locations: list[tuple[str, float, float]],
    distances: list[list[float]],
    color: str,
    show: bool,
) -> None:
    group = folium.FeatureGroup(
        name=f"{name} ({route_cost(route, distances):.2f} km)", show=show
    )
    points = [(locations[index][1], locations[index][2]) for index in route]
    points.append(points[0])
    folium.PolyLine(points, color=color, weight=5, opacity=0.9).add_to(group)
    group.add_to(map_view)


def create_map(output: Path) -> tuple[float, float]:
    locations = load_locations()
    distances = distance_matrix(locations)
    center = (
        sum(latitude for _, latitude, _ in locations) / len(locations),
        sum(longitude for _, _, longitude in locations) / len(locations),
    )
    map_view = folium.Map(location=center, zoom_start=12, control_scale=True)

    points_group = folium.FeatureGroup(name="Lugares", show=True)
    for index, (name, latitude, longitude) in enumerate(locations):
        folium.Marker(
            [latitude, longitude],
            tooltip=f"{index}: {name}",
            popup=f"{name}<br>Latitud: {latitude}<br>Longitud: {longitude}",
        ).add_to(points_group)
    points_group.add_to(map_view)

    complete_graph = folium.FeatureGroup(name="Grafo completo inicial", show=True)
    for first in range(len(locations)):
        for second in range(first + 1, len(locations)):
            folium.PolyLine(
                [
                    [locations[first][1], locations[first][2]],
                    [locations[second][1], locations[second][2]],
                ],
                color="#87939d",
                weight=1,
                opacity=0.25,
            ).add_to(complete_graph)
    complete_graph.add_to(map_view)

    add_route_layer(
        map_view,
        "Orden inicial de la lista",
        list(range(len(locations))),
        locations,
        distances,
        "#e98b32",
        False,
    )
    heuristic = best_heuristic_route(distances)
    add_route_layer(
        map_view, "NN + 2-opt", heuristic, locations, distances, "#167d9a", False
    )
    optimal = exact_route(distances)
    add_route_layer(
        map_view, "Óptimo exacto (Held-Karp)", optimal, locations, distances, "#c73535", False
    )

    folium.LayerControl(collapsed=False).add_to(map_view)
    map_view.fit_bounds(
        [[latitude, longitude] for _, latitude, longitude in locations], padding=(25, 25)
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    map_view.save(str(output))
    return route_cost(heuristic, distances), route_cost(optimal, distances)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Genera un mapa interactivo de las rutas TSP de e5.cpp."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path(__file__).with_name("ruta_arequipa.html"),
        help="archivo HTML de salida (por defecto: ruta_arequipa.html junto al script)",
    )
    arguments = parser.parse_args()
    heuristic_cost, optimal_cost = create_map(arguments.output)
    print(f"Mapa guardado en: {arguments.output.resolve()}")
    print(f"NN + 2-opt: {heuristic_cost:.3f} km")
    print(f"Óptimo exacto (Held-Karp): {optimal_cost:.3f} km")


if __name__ == "__main__":
    main()