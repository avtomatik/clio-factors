"""Explicit metadata for bundled, unmodified historical datasets.

This is a catalog of user-supplied historical snapshots, not an endorsement
of their accuracy, redistribution rights, or currentness.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DatasetSpec:
    slug: str
    title: str
    filename: str
    csv_member: str
    identifier: str
    year: str
    value: str
    description: str | None = None
    source: str | None = "source"
    notes: str = ""


_DATASETS = (
    DatasetSpec(
        "douglas",
        "Douglas: The Theory of Wages",
        "dataset_douglas.zip",
        "douglas.csv",
        "series_id",
        "period",
        "value",
        "description",
        notes="Includes Massachusetts manufacturing production indexes, 1890–1926.",
    ),
    DatasetSpec(
        "cobb-douglas",
        "Cobb & Douglas: A Theory of Production",
        "dataset_usa_cobb-douglas.zip",
        "cobbdouglas.csv",
        "vector",
        "period",
        "value",
        "group1",
        notes="Historical manufacturing capital and employment tables.",
    ),
    DatasetSpec(
        "kendrick",
        "Kendrick: Productivity Trends",
        "dataset_usa_kendrick.zip",
        "kendrick.csv",
        "series_id",
        "period",
        "value",
        "description",
    ),
    DatasetSpec(
        "us-census",
        "Historical Statistics of the United States",
        "dataset_uscb.zip",
        "uscb.csv",
        "series_id",
        "period",
        "value",
        "table",
    ),
    DatasetSpec(
        "brown",
        "Brown: Technical Progress",
        "dataset_usa_brown.zip",
        "brown.csv",
        "series_id",
        "period",
        "value",
        "description_en",
        notes="Contains metadata-only rows with missing numeric values.",
    ),
    DatasetSpec(
        "mcconnell-brue",
        "McConnell & Brue: Economics (2006)",
        "dataset_usa_mc_connell_brue.zip",
        "mcConnellBrue.csv",
        "series",
        "period",
        "value",
        "series",
        notes="Series labels are in Russian.",
    ),
    DatasetSpec(
        "china-turkey-gdp",
        "China/Turkey GDP (source snapshot)",
        "CHN_TUR_GDP.zip",
        "CHN_TUR_GDP.csv",
        "Country Name",
        "Period",
        "Series Name: GDP (current US$)",
        "Country Name",
        source=None,
        notes="Historical nominal GDP; not an inflation-adjusted comparison.",
    ),
)


def all_datasets() -> tuple[DatasetSpec, ...]:
    return _DATASETS


def dataset(slug: str) -> DatasetSpec:
    for item in _DATASETS:
        if item.slug == slug:
            return item
    raise ValueError(f"Unknown dataset {slug!r}; use 'cliofactors catalog' to see options")
