import pytest
from salary_report.cli import suggest_argument_typos, SmartArgumentParser
from salary_report.reports import REPORT_REGISTRY

def test_typo_suggestion_flag(capsys):
    suggest_argument_typos(['--reprt'])
    captured = capsys.readouterr()
    assert "Возможно, вы имели в виду '--report'" in captured.out

def test_invalid_report_value(monkeypatch):
    parser = SmartArgumentParser()
    parser.add_argument('--report', required=True, choices=REPORT_REGISTRY.keys())

    with pytest.raises(SystemExit):
        parser.parse_args(['--report', 'payuot'])

    import io
    import contextlib
    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr):
        try:
            parser.parse_args(['--report', 'payuot'])
        except SystemExit:
            pass
    assert "Возможно, вы имели в виду: 'payout'" in stderr.getvalue()