from salary_report.reader import Employee

def generate_payout_report(data: list[Employee]) -> list[dict]:
    return [
        {
            'name': person['name'],
            'email': person['email'],
            'department': person['department'],
            'hours_worked': person['hours_worked'],
            'hourly_rate': person['hourly_rate'],
            'payout': round(person['hours_worked'] * person['hourly_rate'], 2),
        }
        for person in data
    ]

REPORT_REGISTRY = {
    'payout': generate_payout_report,
}