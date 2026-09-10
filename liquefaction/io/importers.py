from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class ImportResult:
    dataframe: pd.DataFrame
    warnings: list[str]


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed = {c: c.strip() for c in df.columns}
    return df.rename(columns=renamed)


def import_table(path: str, column_map: dict[str, str] | None = None) -> ImportResult:
    if path.lower().endswith(".csv"):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)

    df = _normalize_columns(df)
    if column_map:
        reverse = {v: k for k, v in column_map.items() if v in df.columns}
        df = df.rename(columns=reverse)

    warnings: list[str] = []
    if "depth" in df.columns and df["depth"].duplicated().any():
        warnings.append("Duplicate depth entries found")
    missing = [c for c in ["depth"] if c not in df.columns]
    if missing:
        warnings.append(f"Missing recommended columns: {', '.join(missing)}")
    return ImportResult(dataframe=df, warnings=warnings)
