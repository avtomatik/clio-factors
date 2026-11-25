"""Bundled original data must remain readable, unchanged, and identifiable."""

import pytest

from cliofactors.catalog import all_datasets, dataset
from cliofactors.data import (
    list_series, load_production_frame, load_series, read_table, verify_checksums,
)
from cliofactors.reporting import REFERENCE_SELECTION


def test_catalog_has_seven_unique_slugs():
    items = all_datasets()
    assert len(items) == 7
    assert len({item.slug for item in items}) == len(items)
    assert all(item.filename.endswith('.zip') for item in items)


def test_all_dataset_csv_members_load():
    for spec in all_datasets():
        # Only two columns to minimize memory use on large historical census dataset.
        table = read_table(spec.slug, [spec.identifier, spec.year])
        assert not table.empty
        assert spec.identifier in table


def test_checksums_match_original_archives():
    checks = verify_checksums()
    assert len(checks) == 7
    assert all(checks.values())


def test_reference_series_coverage_and_labels():
    table = list_series('douglas', contains='DT19AS0')
    assert set(table.series_id) == {'DT19AS01', 'DT19AS02', 'DT19AS03'}
    assert set(table.observations) == {37}
    assert set(table.first_year) == {1890}
    assert set(table.last_year) == {1926}
    frame = load_production_frame(
        'douglas', output_id='DT19AS01', labor_id='DT19AS02', capital_id='DT19AS03'
    )
    assert list(frame.columns) == ['output', 'labor', 'capital']
    assert frame.loc[1890].to_dict() == {'output': 72.0, 'labor': 78.0, 'capital': 95.0}
    assert frame.index.name == 'year'


def test_rejects_invalid_identifiers_and_no_overlap():
    with pytest.raises(ValueError, match='Unknown dataset'):
        dataset('bogus')
    with pytest.raises(ValueError, match='not found'):
        load_series('douglas', 'NOT-A-SERIES')
    with pytest.raises(ValueError, match='distinct'):
        load_production_frame('douglas', output_id='DT19AS01', labor_id='DT19AS02', capital_id='DT19AS02')
    with pytest.raises(ValueError, match='No overlapping'):
        load_production_frame(
            'douglas', output_id='DT19AS01', labor_id='DT19AS02', capital_id='DT19AS03',
            start_year=1800, end_year=1810,
        )


def test_reference_recipe_immutable_definition():
    ref = REFERENCE_SELECTION
    assert (ref.slug, ref.output_id, ref.labor_id, ref.capital_id) == (
        'douglas', 'DT19AS01', 'DT19AS02', 'DT19AS03'
    )
