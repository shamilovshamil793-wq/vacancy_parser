import json
import time
import requests
from bs4 import BeautifulSoup

def parse_vacancies(keyword="тестировщик Python", pages=3):
    """Парсит вакансии с hh.ru"""
    all_vacancies = []
    
    for page in range(pages):
        print(f"Парсинг страницы {page + 1}...")
        
        url = "https://hh.ru/search/vacancy"
        params = {
            "text": keyword,
            "page": page,
            "area": 113
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f"Ошибка запроса: {e}")
            break
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Новые селекторы для hh.ru (актуальные)
        vacancy_cards = soup.find_all("div", {"data-qa": "vacancy-serp__vacancy"})
        
        if not vacancy_cards:
            # Альтернативный поиск
            vacancy_cards = soup.find_all("div", class_="serp-item")
        
        if not vacancy_cards:
            print(f"Не найдено карточек на странице {page + 1}")
            continue
        
        print(f"Найдено {len(vacancy_cards)} вакансий на странице")
        
        for card in vacancy_cards:
            try:
                # Название и ссылка
                title_tag = card.find("a", {"data-qa": "vacancy-serp__vacancy-title"})
                if not title_tag:
                    title_tag = card.find("a", class_="serp-item__title")
                
                title = title_tag.text.strip() if title_tag else "Не указано"
                link = title_tag["href"] if title_tag and title_tag.get("href") else ""
                
                # Зарплата
                salary_tag = card.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"})
                if not salary_tag:
                    salary_tag = card.find("span", class_="fake-magister-primary-text")
                salary = salary_tag.text.strip() if salary_tag else "Не указана"
                
                # Компания
                company_tag = card.find("a", {"data-qa": "vacancy-serp__vacancy-employer"})
                if not company_tag:
                    company_tag = card.find("div", class_="vacancy-serp-item__meta-info-company")
                company = company_tag.text.strip() if company_tag else "Не указана"
                
                # Город
                city_tag = card.find("span", {"data-qa": "vacancy-serp__vacancy-address"})
                if not city_tag:
                    city_tag = card.find("div", {"data-qa": "vacancy-serp__vacancy-address"})
                city = city_tag.text.strip() if city_tag else "Не указан"
                
                all_vacancies.append({
                    "title": title,
                    "company": company,
                    "city": city,
                    "salary": salary,
                    "link": link
                })
                
            except Exception as e:
                print(f"Ошибка при парсинге карточки: {e}")
                continue
        
        time.sleep(1)  # Пауза между страницами
    
    return all_vacancies

def save_to_json(data, filename="result.json"):
    """Сохраняет результат в JSON"""
    if not data:
        print("Нет данных для сохранения")
        return
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"\n✅ Сохранено {len(data)} вакансий в {filename}")

def main():
    print("Старт парсинга...")
    
    keyword = input("Введите ключевое слово (Enter = 'тестировщик Python'): ").strip()
    if not keyword:
        keyword = "тестировщик Python"
    
    pages_input = input("Введите количество страниц (Enter = 3): ").strip()
    pages = int(pages_input) if pages_input.isdigit() else 3
    
    vacancies = parse_vacancies(keyword, pages)
    
    if vacancies:
        save_to_json(vacancies)
        print("\n📌 Пример первой вакансии:")
        print(json.dumps(vacancies[0], ensure_ascii=False, indent=2))
    else:
        print("❌ Вакансии не найдены. Попробуйте другое ключевое слово.")

if __name__ == "__main__":
    main()
