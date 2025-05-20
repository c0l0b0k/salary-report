import os
import json
from salary_report.reader import parse_csv, normalize_fields, Employee
from salary_report.reports import REPORT_REGISTRY
from salary_report.cli import get_arguments
from salary_report.output import output_result, print_payout_report

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