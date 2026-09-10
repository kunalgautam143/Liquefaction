from __future__ import annotations

import math


def total_vertical_stress(depth: float, gamma: float) -> float:
    return depth * gamma


def effective_vertical_stress(depth: float, gamma: float, groundwater_depth: float, gamma_w: float = 9.81) -> float:
    if depth <= groundwater_depth:
        return depth * gamma
    dry = groundwater_depth * gamma
    submerged = (depth - groundwater_depth) * max(gamma - gamma_w, 0.1)
    return dry + submerged


def stress_reduction_coefficient(depth: float, mw: float) -> float:
    if depth <= 9.15:
        rd = 1.0 - 0.00765 * depth
    elif depth <= 23:
        rd = 1.174 - 0.0267 * depth
    elif depth <= 30:
        rd = 0.744 - 0.008 * depth
    else:
        rd = 0.5
    scale = 1.0 + 0.02 * (7.5 - mw)
    return max(0.2, min(1.0, rd * scale))


def csr(amax_g: float, sigma_v: float, sigma_v_eff: float, rd: float) -> float:
    if sigma_v_eff <= 0:
        raise ValueError("Effective stress must be > 0 for CSR calculation")
    return 0.65 * amax_g * (sigma_v / sigma_v_eff) * rd


def msf(mw: float) -> float:
    return min(1.8, 10 ** 2.24 / (mw**2.56))


def classify_fs(fs_value: float) -> str:
    return "Liquefaction susceptible" if fs_value < 1.0 else "Not liquefaction susceptible"


def safe_log10(value: float, floor: float = 1e-6) -> float:
    return math.log10(max(value, floor))
