from __future__ import annotations

import argparse
from pathlib import Path

from .engine import LiquefactionEngine
from .io.storage import load_project
from .plotting import create_cpt_plots, create_spt_plots
from .reporting import export_report_pdf, export_results_csv, export_results_excel


def main() -> None:
    parser = argparse.ArgumentParser(description="SPT/CPT liquefaction analysis")
    parser.add_argument("project", help="Path to project json file")
    parser.add_argument("--out", default="output", help="Output folder")
    args = parser.parse_args()

    project = load_project(args.project)
    engine = LiquefactionEngine()
    results = engine.analyze(project)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    export_results_csv(results.spt_results, results.cpt_results, str(out))
    export_results_excel(results.spt_results, results.cpt_results, str(out / "results.xlsx"))
    export_report_pdf(project, results.spt_results, results.cpt_results, str(out / "report.pdf"))
    create_spt_plots(results.spt_results, str(out / "plots"))
    create_cpt_plots(results.cpt_results, str(out / "plots"))

    if results.errors:
        print("Errors:")
        for err in results.errors:
            print(f" - {err}")
    if results.warnings:
        print("Warnings:")
        for wrn in results.warnings:
            print(f" - {wrn}")
    print("Analysis complete. Outputs written to", out)


if __name__ == "__main__":
    main()
