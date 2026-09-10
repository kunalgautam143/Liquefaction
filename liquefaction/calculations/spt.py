from __future__ import annotations

from .common import classify_fs, csr, effective_vertical_stress, msf, stress_reduction_coefficient, total_vertical_stress
from ..models import EarthquakeParameters, SPTRecord


def correction_cb(diameter_mm: float) -> float:
    if diameter_mm <= 115:
        return 1.0
    if diameter_mm <= 150:
        return 1.05
    return 1.15


def correction_cr(rod_length_m: float) -> float:
    if rod_length_m < 3:
        return 0.75
    if rod_length_m < 4:
        return 0.8
    if rod_length_m < 6:
        return 0.85
    if rod_length_m < 10:
        return 0.95
    return 1.0


def correction_cs(has_liner: bool) -> float:
    return 1.0 if has_liner else 1.2


def correction_cn(pa: float, sigma_v_eff: float) -> float:
    if sigma_v_eff <= 0:
        return 1.7
    return min(1.7, (pa / sigma_v_eff) ** 0.5)


def n160(record: SPTRecord, eq: EarthquakeParameters) -> dict[str, float]:
    sigma_v = total_vertical_stress(record.depth, record.gamma)
    sigma_v_eff = effective_vertical_stress(record.depth, record.gamma, eq.groundwater_depth)
    cn = correction_cn(eq.pa, sigma_v_eff)
    ce = record.hammer_energy_ratio / 60.0
    cb = correction_cb(record.borehole_diameter_mm)
    cr = correction_cr(record.rod_length_m)
    cs = correction_cs(record.sampler_liner)
    n1_60 = record.n_value * cn * ce * cb * cr * cs
    return {
        "sigma_v": sigma_v,
        "sigma_v_eff": sigma_v_eff,
        "CN": cn,
        "CE": ce,
        "CB": cb,
        "CR": cr,
        "CS": cs,
        "N160": n1_60,
    }


def n160cs(n160_value: float, fines_content: float) -> float:
    if fines_content <= 5:
        alpha, beta = 0.0, 1.0
    elif fines_content < 35:
        alpha = 5.0 * (fines_content - 5) / 30.0
        beta = 1.0 + 0.1 * (fines_content - 5) / 30.0
    else:
        alpha, beta = 5.0, 1.1
    return alpha + beta * n160_value


def crr75_from_n160cs(value: float) -> float:
    x = min(value, 30.0)
    return 1.0 / (34.0 - x) + x / 135.0 + 50.0 / ((10.0 * x + 45.0) ** 2) - 1.0 / 200.0


def analyze_spt_record(record: SPTRecord, eq: EarthquakeParameters) -> dict[str, float | str]:
    base = n160(record, eq)
    n1cs = n160cs(base["N160"], record.fines_content)
    rd = stress_reduction_coefficient(record.depth, eq.mw)
    csr_val = csr(eq.amax, base["sigma_v"], base["sigma_v_eff"], rd)
    crr75 = crr75_from_n160cs(n1cs)
    msf_val = msf(eq.mw)
    fs = (crr75 / csr_val) * msf_val
    return {
        "depth": record.depth,
        "N": record.n_value,
        **base,
        "FC": record.fines_content,
        "N160cs": n1cs,
        "rd": rd,
        "CSR": csr_val,
        "CRR75": crr75,
        "Mw": eq.mw,
        "MSF": msf_val,
        "FS": fs,
        "status": classify_fs(fs),
        "show_calculation": (
            f"(N1)60 = {record.n_value:.3f} * {base['CN']:.3f} * {base['CE']:.3f} * {base['CB']:.3f} * {base['CR']:.3f} * {base['CS']:.3f}"
        ),
    }
