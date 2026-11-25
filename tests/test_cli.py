import json

import pandas as pd

from cliofactors.cli import main
from cliofactors.reporting import REFERENCE_SELECTION, run_analysis


def test_commands_catalog_series_inspect(capsys):
    assert main(['catalog']) == 0
    assert 'cobb-douglas' in capsys.readouterr().out
    assert main(['series', 'douglas', '--contains', 'DT19AS0']) == 0
    assert 'DT19AS03' in capsys.readouterr().out
    assert main(['inspect', 'douglas', 'DT19AS01', '--limit', '2']) == 0
    assert '1890' in capsys.readouterr().out
    assert main(['verify']) == 0
    assert 'MISMATCH' not in capsys.readouterr().out


def test_error_return_code_without_traceback(capsys):
    assert main(['series', 'absent']) == 2
    assert 'Unknown dataset' in capsys.readouterr().err
    assert main(['inspect', 'douglas', 'bad']) == 2
    assert 'not found' in capsys.readouterr().err


def test_reproduce_outputs_are_complete(tmp_path):
    location = tmp_path / 'test-run'
    assert main(['reproduce', '--out', str(location)]) == 0
    for name in ('manifest.json', 'report.md', 'input.csv', 'levels.csv', 'growth.csv',
                 'levels.json', 'growth.json', 'levels.png', 'growth.png'):
        assert (location/name).is_file(), name
    manifest = json.loads((location/'manifest.json').read_text())
    assert manifest['source_archive'] == 'dataset_douglas.zip'
    assert manifest['missing_years_imputed'] is False
    assert len(manifest['source_sha256']) == 64
    levels = json.loads((location/'levels.json').read_text())
    growth = json.loads((location/'growth.json').read_text())
    assert levels['n'] == 37
    assert growth['n'] == 36
    assert levels['r_squared'] > growth['r_squared']
    assert list(pd.read_csv(location/'input.csv').columns) == ['year', 'output', 'labor', 'capital']
    assert (location/'levels.png').stat().st_size > 10000


def test_custom_fit_and_no_plots(tmp_path):
    target = tmp_path/'custom'
    assert main([
        'fit', '--dataset', 'douglas', '--output-id', 'DT19AS01',
        '--capital-id', 'DT19AS03', '--labor-id', 'DT19AS02', '--spec', 'growth',
        '--out', str(target), '--no-plots',
    ]) == 0
    assert (target/'growth.json').exists()
    assert not (target/'levels.json').exists()
    assert not (target/'growth.png').exists()
    assert 'growth' in (target/'report.md').read_text()


def test_repeatability_of_text_and_csv_outputs(tmp_path):
    a, b = tmp_path/'a',tmp_path/'b'
    run_analysis(REFERENCE_SELECTION, a, plots=False)
    run_analysis(REFERENCE_SELECTION, b, plots=False)
    for name in ('report.md', 'manifest.json', 'levels.json', 'growth.json',
                 'levels.csv', 'growth.csv', 'input.csv'):
        assert (a/name).read_bytes() == (b/name).read_bytes()
