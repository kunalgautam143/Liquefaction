from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from .calculations.cpt import analyze_cpt_record
from .calculations.spt import analyze_spt_record
from .models import Project
from .validation import validate_cpt, validate_earthquake, validate_spt


@dataclass
class AnalysisOutput:
    spt_results: pd.DataFrame = field(default_factory=pd.DataFrame)
    cpt_results: pd.DataFrame = field(default_factory=pd.DataFrame)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class LiquefactionEngine:
    def analyze(self, project: Project) -> AnalysisOutput:
        output = AnalysisOutput()
        eq_report = validate_earthquake(project.earthquake)
        output.errors.extend(eq_report.errors)
        output.warnings.extend(eq_report.warnings)

        spt_rows: list[dict] = []
        for record in sorted(project.data.spt, key=lambda r: r.depth):
            rep = validate_spt(record)
            output.errors.extend(rep.errors)
            output.warnings.extend(rep.warnings)
            if rep.errors:
                continue
            try:
                spt_rows.append(analyze_spt_record(record, project.earthquake))
            except ValueError as exc:
                output.errors.append(f"SPT depth {record.depth}: {exc}")

        cpt_rows: list[dict] = []
        for record in sorted(project.data.cpt, key=lambda r: r.depth):
            rep = validate_cpt(record)
            output.errors.extend(rep.errors)
            output.warnings.extend(rep.warnings)
            if rep.errors:
                continue
            try:
                cpt_rows.append(analyze_cpt_record(record, project.earthquake))
            except ValueError as exc:
                output.errors.append(f"CPT depth {record.depth}: {exc}")

        if spt_rows:
            output.spt_results = pd.DataFrame(spt_rows)
        if cpt_rows:
            output.cpt_results = pd.DataFrame(cpt_rows)

        return output
