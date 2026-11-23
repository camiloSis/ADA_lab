from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "e1.cpp"
RESULT_PATTERN = re.compile(
    r"^\s*(\d+)\s+([0-9]+(?:\.[0-9]+)?)\s+(\d+)\s+(SI|no)\s*$",
)
OPTIMAL_PATTERN = re.compile(r"Optimo exacto[^:]*:\s*([0-9]+(?:\.[0-9]+)?)")


def execute_cpp_results() -> tuple[float, list[dict[str, int | float | str]]]:
    compiler = shutil.which("g++")
    if compiler is None:
        raise RuntimeError("No se encontró g++; instala g++ para compilar e1.cpp.")

    with tempfile.TemporaryDirectory(prefix="lab10-e1-") as temporary_directory:
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

    optimal_match = OPTIMAL_PATTERN.search(output)
    if not optimal_match:
        raise RuntimeError("No se pudo leer el óptimo exacto producido por e1.cpp.")

    results: list[dict[str, int | float | str]] = []
    for line in output.splitlines():
        match = RESULT_PATTERN.match(line)
        if match:
            results.append(
                {
                    "seed": int(match.group(1)),
                    "cost": float(match.group(2)),
                    "iteration": int(match.group(3)),
                    "optimal": match.group(4) == "SI",
                }
            )

    if not results:
        raise RuntimeError("No se pudieron leer los resultados de las semillas.")
    return float(optimal_match.group(1)), results


def create_visualization(
    optimal: float,
    results: list[dict[str, int | float | str]],
    output: Path,
) -> None:
    seeds = [int(result["seed"]) for result in results]
    costs = [float(result["cost"]) for result in results]
    iterations = [int(result["iteration"]) for result in results]
    reaches_optimal = [bool(result["optimal"]) for result in results]

    figure, (cost_axis, iteration_axis) = plt.subplots(
        1,
        2,
        figsize=(12, 4.8),
        gridspec_kw={"width_ratios": [1.35, 1]},
        facecolor="#f7f6f0",
    )

    colors = ["#197c78" if reaches else "#d45b45" for reaches in reaches_optimal]
    bars = cost_axis.bar(seeds, costs, color=colors, width=0.62, edgecolor="#263238", linewidth=0.7)
    cost_axis.axhline(optimal, color="#263238", linewidth=1.2, linestyle=(0, (4, 3)))
    cost_axis.bar_label(bars, labels=[f"{cost:.2f}" for cost in costs], padding=4, fontsize=9)
    cost_axis.set_xlabel("Semilla")
    cost_axis.set_ylabel("Costo")
    cost_axis.set_xticks(seeds)
    cost_axis.set_ylim(min(costs) - 2.5, max(costs) + 3.5)
    cost_axis.grid(axis="y", color="#d9dfdc", linewidth=0.7)
    cost_axis.set_axisbelow(True)
    cost_axis.spines[["top", "right"]].set_visible(False)

    iteration_axis.scatter(seeds, iterations, s=95, c=colors, edgecolor="#263238", linewidth=0.7, zorder=3)
    iteration_axis.plot(seeds, iterations, color="#87939d", linewidth=1, zorder=2)
    for seed, iteration in zip(seeds, iterations):
        iteration_axis.annotate(str(iteration), (seed, iteration), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=8)
    iteration_axis.set_xlabel("Semilla")
    iteration_axis.set_ylabel("Iteración")
    iteration_axis.set_xticks(seeds)
    iteration_axis.set_ylim(-2, 104)
    iteration_axis.grid(color="#d9dfdc", linewidth=0.7)
    iteration_axis.set_axisbelow(True)
    iteration_axis.spines[["top", "right"]].set_visible(False)

    figure.subplots_adjust(wspace=0.3, hspace=0.3)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180, bbox_inches="tight", facecolor=figure.get_facecolor())
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compila e1.cpp y genera la representación visual de sus 10 ejecuciones ILS."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=HERE.parent / "img" / "e1.png",
        help="imagen PNG de salida (por defecto: ../img/e1.png)",
    )
    arguments = parser.parse_args()

    optimal, results = execute_cpp_results()
    create_visualization(optimal, results, arguments.output)

    print(f"Imagen guardada en: {arguments.output.resolve()}")
    print(f"Óptimo exacto: {optimal:.2f}")
    print(f"Semillas exitosas: {sum(bool(result['optimal']) for result in results)} de {len(results)}")


if __name__ == "__main__":
    main()
