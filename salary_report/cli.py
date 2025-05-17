import argparse
import difflib
import sys
from salary_report.reports import REPORT_REGISTRY

# Известные флаги для опечаток
KNOWN_FLAGS = ['--report', '--output-format', '--output-file', '-h']

def suggest_argument_typos(argv: list[str]):
    for arg in argv:
        if arg.startswith('--') and arg not in KNOWN_FLAGS:
            suggestion = difflib.get_close_matches(arg, KNOWN_FLAGS, n=1, cutoff=0.7)
            if suggestion:
                print(f"Возможно, вы имели в виду '{suggestion[0]}' вместо '{arg}'?\n")
                break

# Умный парсер с подсказкой при опечатке значения
class SmartArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        if "invalid choice" in message and "--report" in message:
            wrong_value = message.split("invalid choice: ")[1].split(" (")[0].strip("'\"")
            suggestion = difflib.get_close_matches(wrong_value, REPORT_REGISTRY.keys(), n=1, cutoff=0.7)
            if suggestion:
                print(f"Возможно, вы имели в виду: '{suggestion[0]}'?\n", file=sys.stderr)
        super().error(message)

def get_arguments():
    suggest_argument_typos(sys.argv[1:])

    parser = SmartArgumentParser()
    parser.add_argument('files', nargs='+', help='CSV файлы с данными сотрудников')
    parser.add_argument('--report', required=True, choices=REPORT_REGISTRY.keys(), help='Тип отчёта')
    parser.add_argument('--output-format', choices=['console', 'json'], default='console', help='Формат вывода')
    parser.add_argument('--output-file', help='Файл для сохранения отчёта (только для формата json)')
    return parser.parse_args()
