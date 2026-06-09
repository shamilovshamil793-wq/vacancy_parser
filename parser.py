import json
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

DELAY = 1.5

def get_random_headers():
    ua = UserAgent()
    return {"User-Agent": ua.random}

def parse_vacancies(keyword="тестировщик Python", pages=3):
    all_vacancies = []
    
    for page in range(pages):
        print(f"Парсинг страницы {page + 1}...")
        
        url = "https://hh.ru/search/vacancy"
        params = {
            "text": keyword,
            "page": page,
            "area": 113
        }
        
        try:
            response = requests.get(url, headers=get_random_headers(), params=params, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            break
        
        soup = BeautifulSoup(response.text, "html.parser")
        vacancy_cards = soup.find_all("div", class_="vacancy-card--z_UXteNo7bRGzxWVcL7y")
        
        if not vacancy_cards:
            vacancy_cards = soup.find_all("div", class_="serp-item")
        
        if not vacancy_cards:
            print("Не удалось найти карточки вакансий.")
            break
        
        for card in vacancy_cards:
            try:
                title_tag = card.find("a", class_="bloko-link")
                title = title_tag.text.strip() if title_tag else "Без названия"
                link = title_tag["href"] if title_tag and title_tag.get("href") else ""
                
                salary_tag = card.find("span", class_="fake-magister-primary-text")
                salary = salary_tag.text.strip() if salary_tag else "Не указана"
                
                company_tag = card.find("span", class_="company-name-text")
                company = company_tag.text.strip() if company_tag else "Не указана"
                
                city_tag = card.find("span", {"data-qa": "vacancy-serp__vacancy-address"})
                city = city_tag.text.strip() if city_tag else "Не указан"
                
                all_vacancies.append({
                    "title": title,
                    "company": company,
                    "city": city,
                    "salary": salary,
                    "link": link
                })
            except Exception as e:
                print(f"Ошибка парсинга: {e}")
                continue
        
        time.sleep(DELAY)
    
    return all_vacancies

def save_to_json(data, filename="result.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Сохранено {len(data)} вакансий в {filename}")

def main():
    print("Старт парсинга...")
    keyword = input("Введите ключевое слово (или Enter для 'тестировщик Python'): ").strip()
    if not keyword:
        keyword = "тестировщик Python"
    
    pages = input("Введите количество страниц (по умолчанию 3): ").strip()
    pages = int(pages) if pages.isdigit() else 3
    
    vacancies = parse_vacancies(keyword, pages)
    
    if vacancies:
        save_to_json(vacancies)
        print("\nПример найденной вакансии:")
        print(json.dumps(vacancies[0], ensure_ascii=False, indent=2))
    else:
        print("Вакансии не найдены.")

if __name__ == "__main__":
    main()
