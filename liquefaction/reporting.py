from __future__ import annotations

from pathlib import Path

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .models import Project


def export_results_csv(spt: pd.DataFrame, cpt: pd.DataFrame, out_dir: str) -> list[str]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    files: list[str] = []
    if not spt.empty:
        p = out / "spt_results.csv"
        spt.to_csv(p, index=False)
        files.append(str(p))
    if not cpt.empty:
        p = out / "cpt_results.csv"
        cpt.to_csv(p, index=False)
        files.append(str(p))
    return files


def export_results_excel(spt: pd.DataFrame, cpt: pd.DataFrame, path: str) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        if not spt.empty:
            spt.to_excel(writer, sheet_name="SPT", index=False)
        if not cpt.empty:
            cpt.to_excel(writer, sheet_name="CPT", index=False)


def export_report_pdf(project: Project, spt: pd.DataFrame, cpt: pd.DataFrame, path: str) -> None:
    c = canvas.Canvas(path, pagesize=A4)
    y = 800
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "Liquefaction Potential Assessment Report")
    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Project: {project.info.name}")
    y -= 15
    c.drawString(40, y, f"Client: {project.info.client}")
    y -= 15
    c.drawString(40, y, f"Site: {project.info.site}")
    y -= 15
    c.drawString(40, y, f"Engineer: {project.info.engineer}")
    y -= 25
    c.drawString(40, y, f"Earthquake Mw={project.earthquake.mw}, amax={project.earthquake.amax} g")
    y -= 20
    c.drawString(40, y, f"SPT rows: {len(spt)} | CPT rows: {len(cpt)}")
    y -= 20
    c.drawString(40, y, "Methodology: SPT/CPT liquefaction workflow with correction factors, CSR, CRR, MSF, FS")
    y -= 20
    c.drawString(40, y, "Warnings and applicability should be reviewed in exported result tables.")
    c.showPage()
    c.save()
