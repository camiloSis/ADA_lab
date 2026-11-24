from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "e4.cpp"
ROW = re.compile(r"^(NN|NN \+ 2-opt|ILS|IG)\s+([0-9]+(?:\.[0-9]+)?)\s+([0-9]+(?:\.[0-9]+)?)\s+(?:-?[0-9]+(?:\.[0-9]+)? %|x[0-9]+(?:\.[0-9]+)?)")
PROM = re.compile(r"^(ILS|IG)\s+([0-9]+(?:\.[0-9]+)?)\s+([0-9]+(?:\.[0-9]+)?)\s+-?[0-9]+(?:\.[0-9]+)? %\s*$")

def run():
    compiler = shutil.which("g++")
    if not compiler:
        raise RuntimeError("Se necesita g++")
    with tempfile.TemporaryDirectory() as tmp:
        exe = Path(tmp) / "e4"
        subprocess.run([compiler, "-std=c++17", "-O2", str(SOURCE), "-o", str(exe)], check=True, cwd=HERE)
        output = subprocess.run([str(exe)], check=True, capture_output=True, text=True, cwd=HERE).stdout
    rows = {}
    for line in output.splitlines():
        if m := ROW.match(line.strip()): rows[m.group(1)] = (float(m.group(2)), float(m.group(3)))
    prom = {}
    for line in output.splitlines():
        if m := PROM.match(line.strip()): prom[m.group(1)] = (float(m.group(2)), float(m.group(3)))
    return rows, prom

def main():
    rows, prom = run()
    labels = ["NN", "NN + 2-opt", "ILS", "IG"]
    colors = ["#87939d", "#e5b84b", "#197c78", "#d45b45"]
    costs = [rows[x][0] for x in labels]
    times = [rows[x][1] for x in labels]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), facecolor="#f7f6f0")
    ax1.bar(labels, costs, color=colors, edgecolor="#263238", linewidth=0.7)
    ax1.set_ylabel("Costo")
    ax1.grid(axis="y", color="#d9dfdc", linewidth=0.7)
    ax1.set_axisbelow(True)
    ax1.spines[["top", "right"]].set_visible(False)
    for i, y in enumerate(costs): ax1.text(i, y, f"{y:.2f}", ha="center", va="bottom", fontsize=8)
    ax2.bar(labels, times, color=colors, edgecolor="#263238", linewidth=0.7)
    ax2.set_ylabel("Tiempo (ms)")
    ax2.grid(axis="y", color="#d9dfdc", linewidth=0.7)
    ax2.set_axisbelow(True)
    ax2.spines[["top", "right"]].set_visible(False)
    for i, y in enumerate(times): ax2.text(i, y, f"{y:.1f}", ha="center", va="bottom", fontsize=8)
    fig.tight_layout()
    out = HERE.parent / "img" / "e4.png"
    fig.savefig(out, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(out)

if __name__ == "__main__": main()
