"""Load and validate explicit CSV members of bundled ZIP snapshots.

Never extract archive members to disk; no live downloads or API keys are used.
"""

from __future__ import annotations

from importlib import resources
from io import BytesIO
from zipfile import ZipFile
import hashlib
import json

import pandas as pd

from .catalog import DatasetSpec, dataset


def _archive_bytes(spec: DatasetSpec) -> bytes:
    return resources.files("cliofactors").joinpath("datasets", spec.filename).read_bytes()


def archive_sha256(spec: DatasetSpec) -> str:
    return hashlib.sha256(_archive_bytes(spec)).hexdigest()


def verify_checksums() -> dict[str, bool]:
    """Compare packaged ZIP bytes to original user-provided snapshot hashes."""
    base = resources.files("cliofactors").joinpath("datasets")
    expected = json.loads(base.joinpath("manifest.json").read_text(encoding="utf-8"))
    return {
        name: hashlib.sha256(base.joinpath(name).read_bytes()).hexdigest() == row["sha256"]
        for name, row in expected.items()
    }


def read_table(slug: str, columns: list[str] | None = None) -> pd.DataFrame:
    spec = dataset(slug)
    raw = _archive_bytes(spec)
    with ZipFile(BytesIO(raw)) as z:
        if spec.csv_member not in z.namelist():
            raise ValueError(f"Missing CSV member {spec.csv_member!r} in {spec.filename}")
        with z.open(spec.csv_member) as member:
            # utf-8-sig strips a possible BOM, preserving Unicode descriptions.
            return pd.read_csv(member, encoding="utf-8-sig", usecols=columns, low_memory=False)


def list_series(slug: str, contains: str = "") -> pd.DataFrame:
    """One entry per identifier, with numeric observation count and coverage."""
    spec = dataset(slug)
    columns = list(dict.fromkeys((spec.identifier, spec.year, spec.value, spec.description)))
    table = read_table(slug, columns)
    # Metadata-only records do not constitute observations.
    table = table.dropna(subset=[spec.identifier])
    table[spec.year] = pd.to_numeric(table[spec.year], errors="coerce")
    table[spec.value] = pd.to_numeric(table[spec.value], errors="coerce")
    table = table.dropna(subset=[spec.year, spec.value])
    table[spec.identifier] = table[spec.identifier].astype(str)
    if contains:
        table = table[
            table[spec.identifier].str.contains(contains, case=False, regex=False)
            | table[spec.description or spec.identifier]
            .fillna("")
            .astype(str)
            .str.contains(contains, case=False, regex=False)
        ]
    aggregate = table.groupby(spec.identifier, sort=True).agg(
        observations=(spec.value, "size"),
        first_year=(spec.year, "min"),
        last_year=(spec.year, "max"),
    )
    if spec.description and spec.description != spec.identifier:
        description = (
            table.groupby(spec.identifier)[spec.description]
            .first()
            .rename("description")
        )
        aggregate = aggregate.join(description)
    return aggregate.reset_index().rename(columns={spec.identifier: "series_id"})


def load_series(slug: str, series_id: str) -> pd.Series:
    """Read a single strict annual series; reject duplicate years and bad values.

    Non-numeric metadata rows are excluded, while invalid values for actual
    dated records in the selected series are rejected rather than guessed.
    """
    spec = dataset(slug)
    table = read_table(slug, [spec.identifier, spec.year, spec.value])
    table = table[table[spec.identifier].astype(str) == series_id].copy()
    if table.empty:
        raise ValueError(f"Series {series_id!r} not found in dataset {slug!r}")
    table[spec.year] = pd.to_numeric(table[spec.year], errors="raise")
    table[spec.value] = pd.to_numeric(table[spec.value], errors="raise")
    if table[[spec.year, spec.value]].isna().any().any():
        raise ValueError(f"Missing year or value in {slug}/{series_id}")
    if not (table[spec.year] == table[spec.year].astype(int)).all():
        raise ValueError(f"Non-integer annual year in {slug}/{series_id}")
    if table[spec.year].duplicated().any():
        dup = table.loc[table[spec.year].duplicated(), spec.year].iloc[0]
        raise ValueError(f"Duplicate year {dup} in {slug}/{series_id}")
    output = pd.Series(
        table[spec.value].to_numpy(dtype=float),
        index=pd.Index(table[spec.year].astype(int), name="year"),
        name=series_id,
    ).sort_index()
    return output


def load_production_frame(
    slug: str, *, output_id: str, labor_id: str, capital_id: str,
    start_year: int | None = None, end_year: int | None = None,
) -> pd.DataFrame:
    """Inner-join observations by annual year. No interpolation is performed."""
    if len({output_id, labor_id, capital_id}) != 3:
        raise ValueError("Output, labor, and capital must use three distinct series IDs")
    named = [
        load_series(slug, output_id).rename("output"),
        load_series(slug, labor_id).rename("labor"),
        load_series(slug, capital_id).rename("capital"),
    ]
    frame = pd.concat(named, axis=1, join="inner").sort_index()
    if start_year is not None:
        frame = frame.loc[frame.index >= start_year]
    if end_year is not None:
        frame = frame.loc[frame.index <= end_year]
    if frame.empty:
        raise ValueError("No overlapping years for the requested series/window")
    return frame
