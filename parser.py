cat > parser.py << 'EOF'
import json
import time
import requests

def parse_vacancies_api(keyword="тестировщик Python", pages=3):
    all_vacancies = []
    
    for page in range(pages):
        print(f"Парсинг страницы {page + 1}...")
        
        url = "https://api.hh.ru/vacancies"
        params = {
            "text": keyword,
            "area": 113,
            "page": page,
            "per_page": 20
        }
        
        headers = {"User-Agent": "Mozilla/5.0"}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            data = response.json()
        except Exception as e:
            print(f"Ошибка: {e}")
            break
        
        vacancies = data.get("items", [])
        
        if not vacancies:
            print(f"Вакансии не найдены на странице {page + 1}")
            break
        
        print(f"Найдено {len(vacancies)} вакансий")
        
        for item in vacancies:
            company = item.get("employer", {}).get("name", "Не указана")
            
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
            
            city = item.get("area", {}).get("name", "Не указан")
            
            all_vacancies.append({
                "title": item.get("name", "Не указано"),
                "company": company,
                "city": city,
                "salary": salary,
                "link": item.get("alternate_url", "")
            })
        
        time.sleep(0.5)
    
    return all_vacancies

def save_to_json(data, filename="result.json"):
    if not data:
        print("Нет данных для сохранения")
        return
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"\n✅ Сохранено {len(data)} вакансий в {filename}")

def main():
    print("=" * 50)
    print("Парсер вакансий hh.ru (официальное API)")
    print("=" * 50)
    
    keyword = input("Введите ключевое слово (Enter = 'тестировщик Python'): ").strip()
    if not keyword:
        keyword = "тестировщик Python"
    
    pages_input = input("Введите количество страниц (Enter = 3): ").strip()
    pages = int(pages_input) if pages_input.isdigit() else 3
    
    print(f"\n🔍 Поиск: {keyword}\n")
    
    vacancies = parse_vacancies_api(keyword, pages)
    
    if vacancies:
        save_to_json(vacancies)
        print("\n📌 Пример первой вакансии:")
        print(json.dumps(vacancies[0], ensure_ascii=False, indent=2))
    else:
        print("❌ Вакансии не найдены")

if __name__ == "__main__":
    main()
EOF
