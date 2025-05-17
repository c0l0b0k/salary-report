from salary_report.reports import generate_payout_report


def test_payout_report_calculation():
    data = [{
        'id': '1', 'name': 'Alice', 'email': 'a@a.com',
        'department': 'Sales', 'hours_worked': 160, 'hourly_rate': 50
    }]
    report = generate_payout_report(data)
    assert report[0]['payout'] == 8000.0
    assert report[0]['department'] == 'Sales'


def test_total_payout_sum():
    employees = [
        {
            'id': '1',
            'name': 'Alice',
            'email': 'a@example.com',
            'department': 'HR',
            'hours_worked': 160,
            'hourly_rate': 50
        },
        {
            'id': '2',
            'name': 'Bob',
            'email': 'b@example.com',
            'department': 'HR',
            'hours_worked': 150,
            'hourly_rate': 40
        }
    ]
    report = generate_payout_report(employees)
    payouts = [entry['payout'] for entry in report]
    assert payouts == [8000.0, 6000.0]
    assert sum(payouts) == 14000.0
