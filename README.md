# 📊 Salary Report

Проект для генерации отчётов по сотрудникам на основе CSV-файлов. Позволяет объединять данные из нескольких источников, автоматически нормализует названия колонок, рассчитывает выплаты и формирует отчёты в табличном или JSON-формате.

---

## ⚙️ Возможности

- 📁 Обработка нескольких CSV-файлов одновременно
- 🧠 Автоматическое исправление опечаток в названиях аргументов и колонок
- 🧾 Генерация отчётов с группировкой по отделам
- 📤 Вывод в консоль или JSON-файл
- 📦 Расширяемая архитектура — легко добавлять новые типы отчётов

---

## 🚀 Быстрый старт

### 1. Клонируй репозиторий и перейди в папку проекта

```bash
cd salary_testovoe
```

### 2. Создай и активируй виртуальное окружение

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# или
source venv/bin/activate   # Linux/macOS
```

### 3. Установи зависимости

```bash
pip install -r requirements.txt
```

---

## 📂 Структура проекта

```bash
salary_testovoe/
├── salary_report/           # Исходный код
│   ├── cli.py               # Парсинг аргументов
│   ├── main.py              # Точка входа
│   ├── output.py            # Форматированный вывод
│   ├── reader.py            # Чтение и нормализация CSV
│   ├── reports.py           # Генерация отчётов
│   └── __init__.py
├── tests/                   # Pytest-тесты
│   ├── test_cli.py
│   ├── test_reader.py
│   ├── test_reports.py
│   └── __init__.py
├── data1.csv                # Примеры входных данных
├── data2.csv
├── data3.csv
├── result.json              # Пример отчёта в формате json
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔧 Использование

### 🖥️ Вывод отчёта в консоль:

```bash
python salary_report/main.py data1.csv --report payout
```

### ➕ С несколькими файлами:

```bash
python salary_report/main.py data1.csv data2.csv --report payout
```

### 🧾 Вывод в формате JSON:

```bash
python salary_report/main.py data1.csv --report payout --output-format json
```

### 💾 Сохранение JSON в файл:

```bash
python salary_report/main.py data1.csv --report payout --output-format json --output-file result.json
```

---

## ⚠️ Обработка опечаток

```bash
python salary_report/main.py data.csv --reprt payout
# Вывод: Возможно, вы имели в виду '--report' вместо '--reprt'?
```

```bash
python salary_report/main.py data.csv --report payut
# Вывод: Возможно, вы имели в виду: 'payout'?
```

---

## 📈 Типы отчётов

| Название   | Описание                             |
|------------|--------------------------------------|
| `payout`   | Расчёт выплат (часы × ставка)        |

---

## 🧪 Запуск тестов

### Убедись, что ты в корне проекта:

```bash
cd salary_testovoe
```

### Запуск всех тестов:

```bash
pytest -v
```

---

## 🛠 Как добавить новый отчёт

1. Создай функцию в `reports.py`, возвращающую `List[dict]`.
2. Зарегистрируй её в `REPORT_REGISTRY`.
3. Запусти с `--report new_report_name`.

---

## 📌 Зависимости

Файл `requirements.txt` содержит список зависимостей:

```
pytest
```



---
