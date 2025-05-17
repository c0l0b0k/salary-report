import pytest
from salary_report.reader import normalize_fields, parse_csv

def test_normalization_variants():
    record = {
        'id': '1', 'name': 'Bob', 'email': 'bob@example.com',
        'departmer': 'IT', 'hours_wor': '100', 'rate': '50'
    }
    norm = normalize_fields(record)
    assert norm['department'] == 'IT'
    assert norm['hours_worked'] == 100.0
    assert norm['hourly_rate'] == 50.0

def test_missing_keys_raises():
    with pytest.raises(ValueError):
        normalize_fields({'name': 'A', 'email': 'a@a.com'})

def test_parse_csv(tmp_path):
    file = tmp_path / "data.csv"
    file.write_text("id,email,name,department,hours_worked,hourly_rate\n1,x,x,x,100,20\n")
    result = parse_csv(str(file))
    assert result[0]['id'] == '1'
