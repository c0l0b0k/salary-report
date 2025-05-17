from typing import TypedDict
import difflib
from typing import Optional


class Employee(TypedDict):
    id: str
    name: str
    email: str
    department: str
    hours_worked: float
    hourly_rate: float


REQUIRED_KEYS = {
    'hours_worked': ['hours_worked', 'hours', 'hours_wor'],
    'hourly_rate': ['hourly_rate', 'rate', 'salary'],
    'department': ['department', 'departmer'],
    'id': ['id'],
    'name': ['name'],
    'email': ['email'],
}


def parse_csv(file_path: str) -> list[dict]:
    with open(file_path, encoding='utf-8') as f:
        header = f.readline().strip().split(',')
        return [dict(zip(header, line.strip().split(','))) for line in f]


def find_similar_key(keys: list[str], possible_targets: list[str]) -> Optional[str]:
    for target in possible_targets:
        match = difflib.get_close_matches(target, keys, n=1, cutoff=0.7)
        if match:
            return match[0]
    return None


def normalize_fields(record: dict) -> Employee:
    def resolve_key(possible_keys: list[str]) -> str:
        for key in possible_keys:
            if key in record:
                return key
        suggestion = find_similar_key(list(record.keys()), possible_keys)
        raise ValueError(
            f"Не найдено ни одно из полей {possible_keys}. Возможно, вы имели в виду '{suggestion}'? Доступные ключи: {list(record.keys())}"
        )

    salary_key = resolve_key(REQUIRED_KEYS['hourly_rate'])
    hours_key = resolve_key(REQUIRED_KEYS['hours_worked'])
    department_key = resolve_key(REQUIRED_KEYS['department'])

    return {
        'id': record.get('id', '').strip(),
        'name': record.get('name', '').strip(),
        'email': record.get('email', '').strip(),
        'department': record.get(department_key, '').strip(),
        'hours_worked': float(record.get(hours_key, 0)),
        'hourly_rate': float(record.get(salary_key, 0)),
    }
