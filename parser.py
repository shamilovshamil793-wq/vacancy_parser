import json
import time
import requests

def parse_vacancies_api(keyword="тестировщик Python", pages=3):
    """
    Парсит вакансии через официальное API hh.ru
    Документация: https://github.com/hhru/api
    """
    all_vacancies = []
    
    for page in range(pages):
        print(f"Парсинг страницы {page + 1}...")
        
        url = "https://api.hh.ru/vacancies"
        params = {
            "text": keyword,
            "area": 113,  # 113 = Россия
            "page": page,
            "per_page": 20
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Ошибка запроса к API: {e}")
            break
        
        vacancies = data.get("items", [])
        
        if not vacancies:
            print(f"Вакансии не найдены на странице {page + 1}")
            break
        
        print(f"Найдено {len(vacancies)} вакансий")
        
        for item in vacancies:
            # Получаем название компании
            company = "Не указана"
            if item.get("employer"):
                company = item["employer"].get("name", "Не указана")
            
            # Получаем зарплату
            salary_raw = item.get("salary")
            if salary_raw:
                salary_from = salary_raw.get("from", "")
                salary_to = salary_raw.get("to", "")
                currency = salary_raw.get("currency", "")
                if salary_from and salary_to:
                    salary = f"{salary_from} - {salary_to} {currency}"
                elif salary_from:
                    salary = f"от {salary_from} {currency}"
                elif salary_to:
                    salary = f"до {salary_to} {currency}"
                else:
                    salary = "Не указана"
            else:
                salary = "Не указана"
            
            # Город
            city = "Не указан"
            if item.get("area"):
                city = item["area"].get("name", "Не указан")
            
            all_vacancies.append({
                "title": item.get("name", "Не указано"),
                "company": company,
                "city": city,
                "salary": salary,
                "link": item.get("alternate_url", ""),
                "requirement": item.get("snippet", {}).get("requirement", "").replace("&quot;", '"').replace("&amp;", "&"),
                "responsibility": item.get("snippet", {}).get("responsibility", "").replace("&quot;", '"').replace("&amp;", "&")
            })
        
        time.sleep(0.5)  # Небольшая пауза между запросами
    
    return all_vacancies

def save_to_json(data, filename="result.json"):
    """Сохраняет результат в JSON"""
    if not data:
        print("Нет данных для сохранения")
        return False
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return True

def save_to_csv(data, filename="result.csv"):
    """Сохраняет результат в CSV (удобно для Excel)"""
    if not data:
        return
    
    import csv
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "company", "city", "salary", "link", "requirement", "responsibility"])
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ CSV сохранён: {filename}")

def main():
    print("=" * 50)
    print("Парсер вакансий hh.ru (через официальное API)")
    print("=" * 50)
    
    keyword = input("Введите ключевое слово (Enter = 'тестировщик Python'): ").strip()
    if not keyword:
        keyword = "тестировщик Python"
    
    pages_input = input("Введите количество страниц (Enter = 3, одна страница = 20 вакансий): ").strip()
    pages = int(pages_input) if pages_input.isdigit() else 3
    
    print(f"\n🔍 Ищем '{keyword}'...\n")
    
    vacancies = parse_vacancies_api(keyword, pages)
    
    if vacancies:
        # Сохраняем в JSON
        save_to_json(vacancies)
        print(f"✅ JSON сохранён: result.json ({len(vacancies)} вакансий)")
        
        # Сохраняем в CSV
        save_to_csv(vacancies)
        
        print("\n" + "=" * 50)
        print("📌 Пример первой вакансии:")
        print("=" * 50)
        print(f"Название: {vacancies[0]['title']}")
        print(f"Компания: {vacancies[0]['company']}")
        print(f"Город: {vacancies[0]['city']}")
        print(f"Зарплата: {vacancies[0]['salary']}")
        print(f"Ссылка: {vacancies[0]['link']}")
        if vacancies[0]['requirement']:
            print(f"Требования: {vacancies[0]['requirement'][:200]}...")
    else:
        print("❌ Вакансии не найдены. Попробуйте другое ключевое слово.")

if __name__ == "__main__":
    main()
