from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import date
from typing import Any


@dataclass
class ProjectInfo:
    name: str
    client: str = ""
    site: str = ""
    engineer: str = ""
    project_number: str = ""
    analysis_notes: str = ""
    analysis_date: str = field(default_factory=lambda: date.today().isoformat())


@dataclass
class EarthquakeParameters:
    mw: float
    amax: float
    groundwater_depth: float
    pa: float = 100.0
    g: float = 9.81


@dataclass
class SPTRecord:
    borehole_id: str
    depth: float
    elevation: float | None
    n_value: float
    soil_description: str = ""
    gamma: float = 18.0
    gamma_sat: float | None = None
    fines_content: float = 0.0
    borehole_diameter_mm: float = 100.0
    hammer_energy_ratio: float = 60.0
    rod_length_m: float = 5.0
    sampler_liner: bool = False


@dataclass
class CPTRecord:
    sounding_id: str
    depth: float
    qc: float
    fs: float
    u2: float | None = None
    elevation: float | None = None
    gamma: float = 18.0


@dataclass
class Dataset:
    spt: list[SPTRecord] = field(default_factory=list)
    cpt: list[CPTRecord] = field(default_factory=list)


@dataclass
class Project:
    info: ProjectInfo
    earthquake: EarthquakeParameters
    data: Dataset = field(default_factory=Dataset)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
