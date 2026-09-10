from liquefaction.engine import LiquefactionEngine
from liquefaction.models import CPTRecord, Dataset, EarthquakeParameters, Project, ProjectInfo, SPTRecord


def test_engine_runs_and_returns_tables():
    project = Project(
        info=ProjectInfo(name="Demo"),
        earthquake=EarthquakeParameters(mw=7.5, amax=0.3, groundwater_depth=1.5),
        data=Dataset(
            spt=[SPTRecord(borehole_id="BH-1", depth=3.0, elevation=None, n_value=12, fines_content=15)],
            cpt=[CPTRecord(sounding_id="CPT-1", depth=3.0, qc=5.0, fs=50.0)],
        ),
    )

    out = LiquefactionEngine().analyze(project)
    assert not out.spt_results.empty
    assert not out.cpt_results.empty
    assert "FS" in out.spt_results.columns
    assert "FS" in out.cpt_results.columns
