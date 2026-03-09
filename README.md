# Legal Contract Checker

Простой Python‑инструмент для автоматической проверки текстов договоров по юридическому чек‑листу.

## Возможности

Скрипт:
- проверяет наличие обязательных пунктов в договоре
- ищет риск‑формулировки
- формирует подробный CSV‑отчёт
- создаёт краткое текстовое резюме

## Структура проекта

data/ – входные данные (договоры и чек‑лист)  
src/ – основной Python‑скрипт  
reports/ – создаваемые отчёты  

## Входные данные

### contracts_txt
Текстовые файлы договоров (.txt).

### contract_checklist.csv
Содержит правила проверки.

| rule_id | rule_type | pattern | severity | comment |
|--------|----------|--------|---------|--------|
| 1 | required | Срок | Критично | должен быть срок |

## Запуск

### Windows

python src/check_contracts.py

### macOS / Linux

python3 src/check_contracts.py

## Результат

После запуска создаются файлы:

reports/contract_issues.csv  
reports/contract_summary.txt

CSV можно открыть в Excel.

## Автор

Софья