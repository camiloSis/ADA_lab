from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "e3.cpp"
HEADER12 = re.compile(r"== (TSP de 12 ciudades).*==")
HEADER50 = re.compile(r"== (TSP de 50 ciudades).*==")
ROW12 = re.compile(r"^(Solo si mejora|Acepta peor con 5 %)\s+([0-9]+(?:\.[0-9]+)?)\s+([0-9]+(?:\.[0-9]+)?)\s+([0-9]+(?:\.[0-9]+)?)\s+(\d+/\d+)\s*$")
ROW50 = re.compile(r"^(Solo si mejora|Acepta peor con 5 %)\s+([0-9]+(?:\.[0-9]+)?)\s+([0-9]+(?:\.[0-9]+)?)\s+([0-9]+(?:\.[0-9]+)?)\s+-\s*$")

def run():
    compiler = shutil.which("g++")
    if not compiler:
        raise RuntimeError("Se necesita g++")
    with tempfile.TemporaryDirectory() as tmp:
        exe = Path(tmp) / "e3"
        subprocess.run([compiler, "-std=c++17", "-O2", str(SOURCE), "-o", str(exe)], check=True, cwd=HERE)
        output = subprocess.run([str(exe)], check=True, capture_output=True, text=True, cwd=HERE).stdout
    lines = output.splitlines()
    rows12, rows50 = {}, {}
    section = None
    for line in lines:
        if HEADER12.match(line): section = "12"
        elif HEADER50.match(line): section = "50"
        if section == "12" and (m := ROW12.match(line.strip())):
            rows12[m.group(1)] = tuple(float(x) for x in m.groups()[1:4])
        elif section == "50" and (m := ROW50.match(line.strip())):
            rows50[m.group(1)] = tuple(float(x) for x in m.groups()[1:4])
    return rows12, rows50

def main():
    r12, r50 = run()
    labels = ["Solo si mejora", "Acepta peor con 5 %"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), facecolor="#f7f6f0")
    for ax, data, title in zip(axes, (r12, r50), ("TSP de 12 ciudades", "TSP de 50 ciudades")):
        mean = [data[x][0] for x in labels]
        best = [data[x][1] for x in labels]
        worst = [data[x][2] for x in labels]
        x = np.arange(len(labels))
        ax.bar(x, mean, width=0.58, color=["#197c78", "#d45b45"], edgecolor="#263238", linewidth=0.7)
        ax.errorbar(x, mean, yerr=np.array([np.array(mean)-np.array(best), np.array(worst)-np.array(mean)]), fmt="none", ecolor="#263238", elinewidth=1.2, capsize=4)
        ax.set_xticks(x, ["Estricto", "Acepta peor"])
        ax.set_ylabel("Costo")
        ax.set_title(title, loc="left", fontsize=11, fontweight="bold")
        ax.grid(axis="y", color="#d9dfdc", linewidth=0.7)
        ax.set_axisbelow(True)
        ax.spines[["top", "right"]].set_visible(False)
        for i, y in enumerate(mean): ax.text(i, y, f"{y:.2f}", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    out = HERE.parent / "img" / "e3.png"
    fig.savefig(out, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(out)

if __name__ == "__main__": main()
