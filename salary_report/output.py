from collections import defaultdict
import json
from typing import Optional

def output_result(content: str, output_file: Optional[str]):
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Отчёт сохранён в {output_file}")
    else:
        print(content)

def print_payout_report(report: list[dict]):
    groups = defaultdict(list)
    for r in report:
        groups[r['department']].append(r)

    for dept, employees in groups.items():
        print(dept)
        print(f"{'Name':<20} {'Hours':>7} {'Rate':>7} {'Payout':>12}")
        total_hours = 0
        total_payout = 0
        for emp in employees:
            name = emp['name']
            hours = int(emp.get('hours_worked', 0))
            rate = int(emp.get('hourly_rate', 0))
            payout = emp['payout']
            payout_str = f"${payout:,.0f}"
            print(f"{name:<20} {hours:>7} {rate:>7} {payout_str:>12}")
            total_hours += hours
            total_payout += payout
        total_payout_str = f"${total_payout:,.0f}"
        print(f"{'Total:':<20} {total_hours:>7} {'':>7} {total_payout_str:>12}\n")
