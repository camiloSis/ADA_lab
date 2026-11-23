from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "busqueda_local_iterada.cpp"
INITIAL_PATTERN = re.compile(r"Óptimo local inicial \(NN\+2-opt\): ([0-9]+(?:\.[0-9]+)?)")
IMPROVEMENT_PATTERN = re.compile(r"Iteración (\d+): nuevo mejor costo = ([0-9]+(?:\.[0-9]+)?)")
FINAL_PATTERN = re.compile(r"Costo final: ([0-9]+(?:\.[0-9]+)?)")


def execute_cpp() -> tuple[float, list[tuple[int, float]], float]:
    compiler = shutil.which("g++")
    if compiler is None:
        raise RuntimeError("No se encontró g++; instala g++ para compilar el archivo C++.")

    with tempfile.TemporaryDirectory(prefix="lab10-ils-") as temporary_directory:
        executable = Path(temporary_directory) / "ils"
        subprocess.run([compiler, "-std=c++17", "-O2", str(SOURCE), "-o", str(executable)], check=True, cwd=HERE)
        output = subprocess.run([str(executable)], check=True, capture_output=True, text=True, cwd=HERE).stdout

    initial_match = INITIAL_PATTERN.search(output)
    final_match = FINAL_PATTERN.search(output)
    if not initial_match or not final_match:
        raise RuntimeError("No se pudieron leer los resultados de busqueda_local_iterada.cpp.")

    initial = float(initial_match.group(1))
    improvements = [(int(seed), float(cost)) for seed, cost in IMPROVEMENT_PATTERN.findall(output)]
    final = float(final_match.group(1))
    return initial, improvements, final


def create_visualization(initial: float, improvements: list[tuple[int, float]], final: float, output: Path) -> None:
    iterations = [0] + [iteration for iteration, _ in improvements]
    costs = [initial] + [cost for _, cost in improvements]

    figure, axis = plt.subplots(figsize=(9, 4.8), facecolor="#f7f6f0")
    axis.set_facecolor("#f7f6f0")
    axis.step(iterations, costs, where="post", color="#197c78", linewidth=2.2)
    axis.scatter(iterations, costs, s=38, color="#197c78", edgecolor="#263238", linewidth=0.6, zorder=3)
    axis.axhline(72.21, color="#263238", linewidth=1.2, linestyle=(0, (4, 3)))

    for iteration, cost in improvements:
        axis.annotate(f"{cost:.2f}", (iteration, cost), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=8)

    axis.set_xlabel("Iteración")
    axis.set_ylabel("Costo")
    axis.set_xlim(0, 3)
    axis.set_xticks(range(0, 4))
    axis.grid(axis="both", color="#d9dfdc", linewidth=0.7)
    axis.set_axisbelow(True)
    axis.spines[["top", "right"]].set_visible(False)

    output.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(output, dpi=180, bbox_inches="tight", facecolor=figure.get_facecolor())
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera la convergencia visual del ejercicio ILS resuelto.")
    parser.add_argument("-o", "--output", type=Path, default=HERE.parent / "img" / "busqueda_local_iterada.png")
    arguments = parser.parse_args()

    initial, improvements, final = execute_cpp()
    create_visualization(initial, improvements, final, arguments.output)
    print(f"Imagen guardada en: {arguments.output.resolve()}")
    print(f"Costo inicial: {initial:.2f}")
    print(f"Costo final: {final:.2f}")


if __name__ == "__main__":
    main()
