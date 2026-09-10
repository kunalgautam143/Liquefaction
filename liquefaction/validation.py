from __future__ import annotations

from dataclasses import dataclass, field

from .models import CPTRecord, EarthquakeParameters, SPTRecord


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors


def validate_earthquake(params: EarthquakeParameters) -> ValidationReport:
    report = ValidationReport()
    if params.mw <= 0:
        report.errors.append("Mw must be positive")
    if params.mw < 4 or params.mw > 9.5:
        report.warnings.append("Mw is outside common liquefaction design range (4.0-9.5)")
    if params.amax <= 0:
        report.errors.append("Peak ground acceleration must be positive")
    if params.groundwater_depth < 0:
        report.warnings.append("Groundwater level is above ground; verify input")
    if params.pa <= 0:
        report.errors.append("Reference pressure Pa must be positive")
    return report


def validate_spt(record: SPTRecord) -> ValidationReport:
    report = ValidationReport()
    if record.depth < 0:
        report.errors.append(f"SPT depth cannot be negative: {record.depth}")
    if record.n_value < 0:
        report.errors.append("SPT N-value cannot be negative")
    if record.gamma <= 0:
        report.errors.append("Unit weight must be positive")
    if not (0 <= record.fines_content <= 100):
        report.errors.append("Fines content must be between 0 and 100%")
    if record.rod_length_m <= 0:
        report.errors.append("Rod length must be positive")
    if record.borehole_diameter_mm <= 0:
        report.errors.append("Borehole diameter must be positive")
    return report


def validate_cpt(record: CPTRecord) -> ValidationReport:
    report = ValidationReport()
    if record.depth < 0:
        report.errors.append(f"CPT depth cannot be negative: {record.depth}")
    if record.qc < 0:
        report.errors.append("Cone resistance qc cannot be negative")
    if record.fs < 0:
        report.warnings.append("Sleeve friction fs is negative; verify calibration")
    if record.gamma <= 0:
        report.errors.append("Unit weight must be positive")
    return report
