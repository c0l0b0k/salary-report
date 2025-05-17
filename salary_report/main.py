# import argparse
# import json
# import os
# import difflib
# import sys
# from typing import TypedDict, Callable, Optional
# from collections import defaultdict
#
#
# # Типизированный словарь для строгой структуры
# class Employee(TypedDict):
#     id: str
#     name: str
#     email: str
#     department: str
#     hours_worked: float
#     hourly_rate: float
#
#
# REQUIRED_KEYS = {
#     'hours_worked': ['hours_worked', 'hours', 'hours_wor'],
#     'hourly_rate': ['hourly_rate', 'rate', 'salary'],
#     'department': ['department', 'departmer'],
#     'id': ['id'],
#     'name': ['name'],
#     'email': ['email'],
# }
#
#
# # Класс с умной подсказкой для argparse
# class SmartArgumentParser(argparse.ArgumentParser):
#     def error(self, message):
#         if "invalid choice" in message and "--report" in message:
#             wrong_value = message.split("invalid choice: ")[1].split(" (")[0].strip("'\"")
#             suggestion = difflib.get_close_matches(wrong_value, REPORT_REGISTRY.keys(), n=1, cutoff=0.7)
#             if suggestion:
#                 print(f"Возможно, вы имели в виду: '{suggestion[0]}'?\n", file=sys.stderr)
#         super().error(message)
#
#
# # Подсказка по опечаткам аргументов
# KNOWN_FLAGS = ['--report', '--output-format', '--output-file', '-h']
#
#
# def suggest_argument_typos(argv: list[str]):
#     for arg in argv:
#         if arg.startswith('--') and arg not in KNOWN_FLAGS:
#             suggestion = difflib.get_close_matches(arg, KNOWN_FLAGS, n=1, cutoff=0.7)
#             if suggestion:
#                 print(f"Возможно, вы имели в виду '{suggestion[0]}' вместо '{arg}'?\n")
#                 break
#
#
# def find_similar_key(keys: list[str], possible_targets: list[str]) -> Optional[str]:
#     for target in possible_targets:
#         match = difflib.get_close_matches(target, keys, n=1, cutoff=0.7)
#         if match:
#             return match[0]
#     return None
#
#
# def parse_csv(file_path: str) -> list[dict]:
#     with open(file_path, encoding='utf-8') as f:
#         header = f.readline().strip().split(',')
#         data = []
#         for line in f:
#             row = dict(zip(header, line.strip().split(',')))
#             data.append(row)
#         return data
#
#
# def normalize_fields(record: dict) -> Employee:
#     def resolve_key(possible_keys: list[str]) -> str:
#         for key in possible_keys:
#             if key in record:
#                 return key
#         suggestion = find_similar_key(list(record.keys()), possible_keys)
#         raise ValueError(
#             f"Не найдено ни одно из полей {possible_keys}. Возможно, вы имели в виду '{suggestion}'? Доступные ключи: {list(record.keys())}"
#         )
#
#     salary_key = resolve_key(REQUIRED_KEYS['hourly_rate'])
#     hours_key = resolve_key(REQUIRED_KEYS['hours_worked'])
#     department_key = resolve_key(REQUIRED_KEYS['department'])
#
#     try:
#         return {
#             'id': record.get('id', '').strip(),
#             'name': record.get('name', '').strip(),
#             'email': record.get('email', '').strip(),
#             'department': record.get(department_key, '').strip(),
#             'hours_worked': float(record.get(hours_key, 0)),
#             'hourly_rate': float(record.get(salary_key, 0)),
#         }
#     except ValueError as e:
#         raise ValueError(f"Ошибка преобразования типов: {record}. {e}")
#
#
# def generate_payout_report(data: list[Employee]) -> list[dict]:
#     return [
#         {
#             'name': person['name'],
#             'email': person['email'],
#             'department': person['department'],
#             'hours_worked': person['hours_worked'],
#             'hourly_rate': person['hourly_rate'],
#             'payout': round(person['hours_worked'] * person['hourly_rate'], 2),
#         }
#         for person in data
#     ]
#
#
# def print_payout_report(report: list[dict]):
#     groups = defaultdict(list)
#     for r in report:
#         groups[r['department']].append(r)
#
#     for dept, employees in groups.items():
#         print(dept)
#         print(f"{'Name':<20} {'Hours':>7} {'Rate':>7} {'Payout':>12}")
#         total_hours = 0
#         total_payout = 0
#         for emp in employees:
#             name = emp['name']
#             hours = int(emp.get('hours_worked', 0))
#             rate = int(emp.get('hourly_rate', 0))
#             payout = emp['payout']
#             payout_str = f"${payout:,.0f}"
#             print(f"{name:<20} {hours:>7} {rate:>7} {payout_str:>12}")
#             total_hours += hours
#             total_payout += payout
#         total_payout_str = f"${total_payout:,.0f}"
#         print(f"{'Total:':<20} {total_hours:>7} {'':>7} {total_payout_str:>12}\n")
#
#
# # Реестр доступных отчётов
# REPORT_REGISTRY: dict[str, Callable[[list[Employee]], list[dict]]] = {
#     'payout': generate_payout_report,
# }
#
#
# def output_result(content: str, output_file: Optional[str]):
#     if output_file:
#         with open(output_file, 'w', encoding='utf-8') as f:
#             f.write(content)
#         print(f"Отчёт сохранён в {output_file}")
#     else:
#         print(content)
#
#
# def main():
#     suggest_argument_typos(sys.argv[1:])
#
#     parser = SmartArgumentParser()
#     parser.add_argument('files', nargs='+', help='CSV файлы с данными сотрудников')
#     parser.add_argument('--report', required=True, choices=REPORT_REGISTRY.keys(), help='Тип отчёта')
#     parser.add_argument('--output-format', choices=['console', 'json'], default='console', help='Формат вывода')
#     parser.add_argument('--output-file', help='Файл для сохранения отчёта (только для формата json)')
#     args = parser.parse_args()
#
#     all_records: list[Employee] = []
#     for file in args.files:
#         if not os.path.isfile(file):
#             print(f"Файл не найден: {file}")
#             continue
#         try:
#             raw_data = parse_csv(file)
#             normalized_data = [normalize_fields(record) for record in raw_data]
#             all_records.extend(normalized_data)
#         except Exception as e:
#             print(f"Ошибка при обработке файла {file}: {e}")
#
#     report_fn = REPORT_REGISTRY.get(args.report)
#     if not report_fn:
#         print(f"Неизвестный тип отчёта: {args.report}")
#         return
#
#     try:
#         report = report_fn(all_records)
#         if args.output_format == 'json':
#             output = json.dumps(report, indent=2, ensure_ascii=False)
#             output_result(output, args.output_file)
#         else:
#             print_payout_report(report)
#     except Exception as e:
#         print(f"Ошибка генерации отчёта: {e}")
#
#
# if __name__ == '__main__':
#     main()

import os
import json
from reader import parse_csv, normalize_fields, Employee
from reports import REPORT_REGISTRY
from cli import get_arguments
from output import output_result, print_payout_report

def main():
    args = get_arguments()

    all_records: list[Employee] = []
    for file in args.files:
        if not os.path.isfile(file):
            print(f"Файл не найден: {file}")
            continue
        try:
            raw_data = parse_csv(file)
            normalized_data = [normalize_fields(record) for record in raw_data]
            all_records.extend(normalized_data)
        except Exception as e:
            print(f"Ошибка при обработке файла {file}: {e}")

    report_fn = REPORT_REGISTRY.get(args.report)
    if not report_fn:
        print(f"Неизвестный тип отчёта: {args.report}")
        return

    try:
        report = report_fn(all_records)
        if args.output_format == 'json':
            output = json.dumps(report, indent=2, ensure_ascii=False)
            output_result(output, args.output_file)
        else:
            print_payout_report(report)
    except Exception as e:
        print(f"Ошибка генерации отчёта: {e}")

if __name__ == '__main__':
    main()