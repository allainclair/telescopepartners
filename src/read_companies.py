import csv

from src.config import COMPANY_NAMES_PATH, COMPANY_NAME_URLS_EMPLOYEES_PATH


def read_companies(file_path: str = COMPANY_NAMES_PATH) -> list[str]:
    companies = []
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            companies.append(row[0])
    return companies


def save_companies(
    company_urls_employees: list[tuple[str, str, int]],
    file_path: str = COMPANY_NAME_URLS_EMPLOYEES_PATH,
) -> None:
    with open(file_path, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["company", "url", "employees"])
        for company, url, employees in company_urls_employees:
            writer.writerow([company, url, employees])
