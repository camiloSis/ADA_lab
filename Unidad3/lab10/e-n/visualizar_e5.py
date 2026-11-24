from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "e5.cpp"
LOCATION = re.compile(r'^\s*\{"([^"]+)"\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\}', re.MULTILINE)
ROUTE_ROW = re.compile(r'^\s*\d+\.\s+(.+?)\s+->\s+(.+?)\s+[0-9]', re.MULTILINE)
COST_ROW = re.compile(r"Costo: ([0-9]+(?:\.[0-9]+)?) km \| Solo NN: ([0-9]+(?:\.[0-9]+)?) km \([^)]*\) \| NN\+2opt: ([0-9]+(?:\.[0-9]+)?) km")

def execute() -> tuple[list[str], list[tuple[float, float]], list[str], tuple[float, float, float]]:
    compiler = shutil.which("g++")
    if not compiler:
        raise RuntimeError("Se necesita g++")
    with tempfile.TemporaryDirectory() as tmp:
        exe = Path(tmp) / "e5"
        subprocess.run([compiler, "-std=c++17", "-O2", str(SOURCE), "-o", str(exe)], check=True, cwd=HERE)
        output = subprocess.run([str(exe)], check=True, capture_output=True, text=True, cwd=HERE).stdout

    source = SOURCE.read_text(encoding="utf-8")
    start = source.index("const vector<Lugar> LUGARES")
    end = source.index("};", start)
    entries = LOCATION.findall(source[start:end])
    entries = entries[:18]
    names = [name for name, _, _ in entries]
    coordinates = [(float(lat), float(lon)) for _, lat, lon in entries]

    route_names = []
    for first, second in ROUTE_ROW.findall(output):
        route_names.append(first.strip())
        if second.strip() not in route_names:
            route_names.append(second.strip())
    route_names = route_names[:18]

    cost_match = re.search(r"ILS\s+mejor\s+([0-9]+(?:\.[0-9]+)?)", output)
    nn_match = re.search(r"Solo Nearest Neighbor .*?:\s*([0-9]+(?:\.[0-9]+)?)", output)
    nn2_match = re.search(r"NN \+ 2-opt \(desde Plaza de Armas\):\s*([0-9]+(?:\.[0-9]+)?)", output)
    if not (cost_match and nn_match and nn2_match):
        raise RuntimeError("No se pudieron leer los costos")
    cost_values = (float(cost_match.group(1)), float(nn_match.group(1)), float(nn2_match.group(1)))
    return names, coordinates, route_names, cost_values

def main():
    names, coordinates, route_names, costs = execute()
    name_index = {name: i for i, name in enumerate(names)}

    route = [name_index[name] for name in route_names if name in name_index]
    if len(route) < 2:
        route = list(range(len(names)))
    route = route + [route[0]]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2), facecolor="#f7f6f0")
    ax1.set_facecolor("#f7f6f0")
    xs = [coordinates[i][1] for i in route]
    ys = [coordinates[i][0] for i in route]
    ax1.plot(xs, ys, "-o", color="#197c78", linewidth=1.8, markersize=5, markeredgecolor="#263238", markeredgewidth=0.5)
    for i, (lon, lat) in enumerate([(coordinates[j][1], coordinates[j][0]) for j in route[:-1]]):
        ax1.annotate(str(i + 1), (lon, lat), xytext=(3, 3), textcoords="offset points", fontsize=7)
    ax1.set_xlabel("Longitud")
    ax1.set_ylabel("Latitud")
    ax1.grid(color="#d9dfdc", linewidth=0.7)
    ax1.set_axisbelow(True)
    ax1.spines[["top", "right"]].set_visible(False)

    labels = ["ILS/IG", "NN", "NN+2-opt"]
    values = [costs[0], costs[1], costs[2]]
    ax2.bar(labels, values, color=["#197c78", "#87939d", "#e5b84b"], edgecolor="#263238", linewidth=0.7)
    ax2.set_ylabel("Costo (km)")
    ax2.grid(axis="y", color="#d9dfdc", linewidth=0.7)
    ax2.set_axisbelow(True)
    ax2.spines[["top", "right"]].set_visible(False)
    for i, y in enumerate(values): ax2.text(i, y, f"{y:.3f}", ha="center", va="bottom", fontsize=9)

    fig.tight_layout()
    out = HERE.parent / "img" / "e5.png"
    fig.savefig(out, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(out)

if __name__ == "__main__": main()
