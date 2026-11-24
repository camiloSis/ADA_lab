from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "e2.cpp"
ROW = re.compile(r"^\s*(\d+)\s+([0-9]+(?:\.[0-9]+)?)\s+([0-9]+(?:\.[0-9]+)?)\s+([0-9]+(?:\.[0-9]+)?)\s+(\d+/\d+)\s+(-?[0-9]+(?:\.[0-9]+)?)%\s*$")

def run() -> tuple[list[int], list[float], list[float], list[str], list[float]]:
    compiler = shutil.which("g++")
    if not compiler:
        raise RuntimeError("Se necesita g++")
    with tempfile.TemporaryDirectory() as tmp:
        exe = Path(tmp) / "e2"
        subprocess.run([compiler, "-std=c++17", "-O2", str(SOURCE), "-o", str(exe)], check=True, cwd=HERE)
        output = subprocess.run([str(exe)], check=True, capture_output=True, text=True, cwd=HERE).stdout
    rows = [m.groups() for line in output.splitlines() if (m := ROW.match(line))]
    if not rows:
        raise RuntimeError("No se pudieron leer los resultados")
    d = [int(r[0]) for r in rows]
    mean = [float(r[1]) for r in rows]
    best = [float(r[2]) for r in rows]
    worst = [float(r[3]) for r in rows]
    hits = [r[4] for r in rows]
    gap = [float(r[5]) for r in rows]
    return d, mean, best, worst, hits, gap

def main():
    d, mean, best, worst, hits, gap = run()
    fig, ax = plt.subplots(figsize=(9.5, 5), facecolor="#f7f6f0")
    ax.set_facecolor("#f7f6f0")
    ax.plot(d, mean, marker="o", linewidth=2.2, markersize=7, color="#197c78")
    ax.fill_between(d, best, worst, color="#197c78", alpha=0.12)
    ax.scatter(d, best, s=35, color="#263238", zorder=3)
    ax.axhline(72.21, color="#d45b45", linewidth=1.2, linestyle=(0, (4, 3)))
    for x, y, h in zip(d, mean, hits):
        ax.annotate(f"{y:.2f}\n{h}", (x, y), xytext=(0, 10), textcoords="offset points", ha="center", fontsize=8)
    ax.set_xlabel("Ciudades destruidas (d)")
    ax.set_ylabel("Costo promedio")
    ax.set_xticks(d)
    ax.grid(axis="both", color="#d9dfdc", linewidth=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    out = HERE.parent / "img" / "e2.png"
    fig.savefig(out, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(out)

if __name__ == "__main__": main()
