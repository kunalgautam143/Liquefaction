from __future__ import annotations

import math

from .common import classify_fs, csr, effective_vertical_stress, msf, safe_log10, stress_reduction_coefficient, total_vertical_stress
from ..models import CPTRecord, EarthquakeParameters


def iterate_n(ic: float, sigma_v_eff: float, pa: float) -> float:
    return min(1.0, max(0.5, 0.381 * ic + 0.05 * (sigma_v_eff / pa) - 0.15))


def cq(pa: float, sigma_v_eff: float, n: float) -> float:
    if sigma_v_eff <= 0:
        return 1.7
    return min(1.7, (pa / sigma_v_eff) ** n)


def soil_behavior_index(q: float, f: float) -> float:
    return math.sqrt((3.47 - safe_log10(q)) ** 2 + (safe_log10(f) + 1.22) ** 2)


def kc_from_ic(ic: float) -> float:
    if ic <= 1.64:
        return 1.0
    if ic > 2.6:
        return 1.0
    return -0.403 * ic**4 + 5.581 * ic**3 - 21.63 * ic**2 + 33.75 * ic - 17.88


def crr75_from_qc1ncs(qc1ncs: float) -> float:
    x = min(max(qc1ncs, 1.0), 160.0)
    return math.exp(x / 540.0 + (x / 67.0) ** 2 - (x / 80.0) ** 3 + (x / 114.0) ** 4 - 3.0)


def analyze_cpt_record(record: CPTRecord, eq: EarthquakeParameters) -> dict[str, float | str]:
    sigma_v = total_vertical_stress(record.depth, record.gamma)
    sigma_v_eff = effective_vertical_stress(record.depth, record.gamma, eq.groundwater_depth)
    q_net = max(record.qc * 1000.0 - sigma_v, 1e-6)
    n_val = 1.0
    q = 1.0
    f = 1.0
    ic = 2.6
    for _ in range(15):
        c_q = cq(eq.pa, sigma_v_eff, n_val)
        q = (q_net / eq.pa) * c_q
        f = max((record.fs / q_net) * 100.0, 1e-6)
        ic_new = soil_behavior_index(q, f)
        n_new = iterate_n(ic_new, sigma_v_eff, eq.pa)
        if abs(n_new - n_val) < 1e-4:
            ic = ic_new
            n_val = n_new
            break
        ic = ic_new
        n_val = n_new
    c_q = cq(eq.pa, sigma_v_eff, n_val)
    qc1n = (record.qc * 1000.0 / eq.pa) * c_q
    kc = kc_from_ic(ic)
    qc1ncs = qc1n * kc
    rd = stress_reduction_coefficient(record.depth, eq.mw)
    csr_val = csr(eq.amax, sigma_v, sigma_v_eff, rd)
    crr75 = crr75_from_qc1ncs(qc1ncs)
    msf_val = msf(eq.mw)
    fs = (crr75 / csr_val) * msf_val
    return {
        "depth": record.depth,
        "qc": record.qc,
        "fs": record.fs,
        "sigma_v": sigma_v,
        "sigma_v_eff": sigma_v_eff,
        "Q": q,
        "F": f,
        "Ic": ic,
        "n": n_val,
        "CQ": c_q,
        "qc1N": qc1n,
        "Kc": kc,
        "qc1Ncs": qc1ncs,
        "rd": rd,
        "CSR": csr_val,
        "CRR75": crr75,
        "Mw": eq.mw,
        "MSF": msf_val,
        "FS": fs,
        "status": classify_fs(fs),
        "show_calculation": f"qc1N = ({record.qc:.3f} MPa*1000/{eq.pa:.1f})*{c_q:.3f}; (qc1N)cs={qc1n:.3f}*{kc:.3f}",
    }
