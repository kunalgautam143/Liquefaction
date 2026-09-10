from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def _plot_depth(df: pd.DataFrame, xcol: str, path: Path, title: str) -> None:
    fig, ax = plt.subplots(figsize=(5, 7))
    ax.plot(df[xcol], df["depth"], marker="o", linewidth=1)
    ax.invert_yaxis()
    ax.set_xlabel(xcol)
    ax.set_ylabel("Depth (m)")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def create_spt_plots(df: pd.DataFrame, out_dir: str) -> list[str]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    cols = ["N", "N160", "N160cs", "CSR", "CRR75", "FS"]
    files: list[str] = []
    for col in cols:
        if col in df.columns:
            p = out / f"spt_{col.lower()}.png"
            _plot_depth(df, col, p, f"SPT {col} vs Depth")
            files.append(str(p))
    return files


def create_cpt_plots(df: pd.DataFrame, out_dir: str) -> list[str]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    cols = ["qc", "fs", "Ic", "qc1N", "qc1Ncs", "CSR", "CRR75", "FS"]
    files: list[str] = []
    for col in cols:
        if col in df.columns:
            p = out / f"cpt_{col.lower()}.png"
            _plot_depth(df, col, p, f"CPT {col} vs Depth")
            files.append(str(p))
    return files
