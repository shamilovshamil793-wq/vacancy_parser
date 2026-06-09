import json
import requests
import time
from datetime import datetime

def parse_jsonplaceholder(resource="posts", limit=20):
    """
    Парсит тестовые данные с JSONPlaceholder
    Документация: https://jsonplaceholder.typicode.com/
    """
    url = f"https://jsonplaceholder.typicode.com/{resource}"
    
    print(f"📡 Запрос к {url}...")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    limited_data = data[:limit]
    
    # Форматируем данные в зависимости от ресурса
    formatted = []
    for item in limited_data:
        if resource == "posts":
            formatted.append({
                "id": item["id"],
                "title": item["title"],
                "body": item["body"][:200],
                "type": "post"
            })
        elif resource == "comments":
            formatted.append({
                "id": item["id"],
                "name": item["name"],
                "email": item["email"],
                "body": item["body"][:150],
                "type": "comment"
            })
        elif resource == "todos":
            formatted.append({
                "id": item["id"],
                "title": item["title"],
                "completed": item["completed"],
                "type": "task"
            })
    
    return formatted

def main():
    print("=" * 50)
    print("📡 Парсер тестового API (JSONPlaceholder)")
    print("=" * 50)
    
    print("\nДоступные ресурсы:")
    print("  1 — Посты (posts)")
    print("  2 — Комментарии (comments)")
    print("  3 — Задачи (todos)")
    
    choice = input("\n👉 Выберите ресурс (Enter = 1): ").strip()
    
    resources = {"1": "posts", "2": "comments", "3": "todos"}
    resource = resources.get(choice, "posts")
    
    limit = input("👉 Количество записей (Enter = 20): ").strip()
    limit = int(limit) if limit.isdigit() else 20
    
    print(f"\n⏳ Парсинг {resource}...\n")
    
    data = parse_jsonplaceholder(resource, limit)
    
    if data:
        # Сохраняем в JSON
        filename = f"api_{resource}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"✅ Сохранено {len(data)} записей в {filename}")
        print("\n📌 Пример:")
        print(json.dumps(data[0], ensure_ascii=False, indent=2))
    else:
        print("❌ Данные не получены")

if __name__ == "__main__":
    main()
