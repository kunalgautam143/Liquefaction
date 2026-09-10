# Liquefaction

Professional SPT and CPT liquefaction potential analysis software with a calculation-first architecture.

## Implemented architecture

- `liquefaction/calculations`: engineering equations (SPT, CPT, CSR/MSF)
- `liquefaction/validation.py`: strong input validation and warnings
- `liquefaction/engine.py`: independent calculation engine (testable without UI)
- `liquefaction/io`: project persistence and Excel/CSV imports
- `liquefaction/plotting.py`: depth profile plots
- `liquefaction/reporting.py`: CSV/Excel/PDF report exports
- `liquefaction/ui/app.py`: desktop dashboard UI

## Methodology/equation panel (implemented)

SPT:
- `(N1)60 = Nm * CN * CE * CB * CR * CS`
- `CN = min(1.7, sqrt(Pa/sigma'v))`
- fines correction uses piecewise FC ranges (<=5, 5-35, >=35)
- `CRR7.5` from corrected `(N1)60cs`

CPT:
- `Q`, `F`, `Ic` and iterative `n`
- `CQ = min(1.7, (Pa/sigma'v)^n)`
- `qc1N = (qc/Pa) * CQ`
- `(qc1N)cs = Kc * qc1N`

Common:
- `CSR = 0.65 * (amax/g) * (sigma_v/sigma'_v) * rd`
- depth-dependent `rd`
- `MSF` from `Mw`
- `FS = (CRR7.5 / CSR) * MSF`

Every result row includes a `show_calculation` trace string for transparency.

## Quick start

```bash
python -m pip install -e .[dev]
pytest
```

### Run desktop app

```bash
liquefaction-ui
```

### Run CLI engine/export pipeline

```bash
liquefaction-cli /absolute/path/to/project.json --out /absolute/path/to/output
```

## Project JSON format

Use `Project`, `EarthquakeParameters`, `SPTRecord`, and `CPTRecord` structures from `liquefaction/models.py`.
