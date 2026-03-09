import os
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHECKLIST_FILE = os.path.join(BASE_DIR, "data", "contract_checklist.csv")
CONTRACTS_FOLDER = os.path.join(BASE_DIR, "data", "contracts_txt")
REPORT_ISSUES = os.path.join(BASE_DIR, "reports", "contract_issues.csv")
REPORT_SUMMARY = os.path.join(BASE_DIR, "reports", "contract_summary.txt")

def load_rules():
    rules = []
    with open(CHECKLIST_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rules.append(row)
    return rules

def load_contracts():
    contracts = []
    for file in os.listdir(CONTRACTS_FOLDER):
        if file.endswith(".txt"):
            path = os.path.join(CONTRACTS_FOLDER, file)
            with open(path, encoding="utf-8") as f:
                text = f.read().lower()
            contracts.append((file, text))
    return contracts

def check_contract(contract_file, text, rules):
    results = []
    for rule in rules:
        pattern = rule["pattern"].lower()

        if rule["rule_type"] == "required":
            status = "FOUND" if pattern in text else "MISSING"
        else:
            status = "FOUND_RISK" if pattern in text else "NOT_FOUND"

        results.append({
            "contract_file": contract_file,
            "rule_id": rule["rule_id"],
            "rule_type": rule["rule_type"],
            "severity": rule["severity"],
            "pattern": rule["pattern"],
            "status": status,
            "comment": rule["comment"]
        })

    return results

def save_issues(all_results):
    os.makedirs(os.path.dirname(REPORT_ISSUES), exist_ok=True)

    with open(REPORT_ISSUES, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "contract_file",
            "rule_id",
            "rule_type",
            "severity",
            "pattern",
            "status",
            "comment"
        ]

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in all_results:
            writer.writerow(row)

def create_summary(all_results):
    contracts = set(r["contract_file"] for r in all_results)

    critical_count = sum(
        1 for r in all_results
        if r["severity"] == "Критично"
        and (r["status"] == "MISSING" or r["status"] == "FOUND_RISK")
    )

    lines = []
    lines.append(f"Проверено договоров: {len(contracts)}")
    lines.append(f"Критичных замечаний: {critical_count}\n")

    for contract in contracts:
        lines.append(f"Договор: {contract}")

        issues = [
            r for r in all_results
            if r["contract_file"] == contract
            and (r["status"] == "MISSING" or r["status"] == "FOUND_RISK")
        ]

        for issue in issues[:5]:
            lines.append(f"- {issue['severity']}: {issue['comment']} ({issue['status']})")

        lines.append("")

    with open(REPORT_SUMMARY, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def main():
    rules = load_rules()
    contracts = load_contracts()

    all_results = []

    for contract_file, text in contracts:
        results = check_contract(contract_file, text, rules)
        all_results.extend(results)

    save_issues(all_results)
    create_summary(all_results)

    print("Проверка завершена. Отчёты созданы в папке reports/")

if __name__ == "__main__":
    main()