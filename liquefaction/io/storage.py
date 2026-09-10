from __future__ import annotations

import json

from ..models import CPTRecord, Dataset, EarthquakeParameters, Project, ProjectInfo, SPTRecord


def save_project(project: Project, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(project.to_dict(), f, indent=2)


def load_project(path: str) -> Project:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    info = ProjectInfo(**data["info"])
    eq = EarthquakeParameters(**data["earthquake"])
    spt = [SPTRecord(**row) for row in data.get("data", {}).get("spt", [])]
    cpt = [CPTRecord(**row) for row in data.get("data", {}).get("cpt", [])]
    return Project(info=info, earthquake=eq, data=Dataset(spt=spt, cpt=cpt))
