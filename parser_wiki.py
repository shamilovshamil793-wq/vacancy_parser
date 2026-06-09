import json
import requests
from urllib.parse import quote

def search_wikipedia(query="Software testing"):
    """Ищет статьи в Wikipedia через официальное API"""
    
    # Кодируем запрос для URL
    encoded_query = quote(query)
    
    # Правильный API URL для русской Wikipedia
    search_url = f"https://ru.wikipedia.org/w/api.php"
    
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "utf8": 1,
        "origin": "*"  # Важно для CORS
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    print(f"📡 Поиск: {query}")
    print(f"📡 URL: {search_url}")
    
    try:
        response = requests.get(search_url, headers=headers, params=params, timeout=15)
        print(f"   HTTP статус: {response.status_code}")
        
        # Проверяем, что ответ — это JSON
        if response.status_code != 200:
            print(f"   Ошибка: статус {response.status_code}")
            return []
        
        # Пробуем распарсить JSON
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print(f"   Ошибка JSON: {e}")
            print(f"   Первые 200 символов ответа: {response.text[:200]}")
            return []
        
        # Извлекаем результаты
        search_results = data.get("query", {}).get("search", [])
        
        if not search_results:
            print("   Ничего не найдено")
            return []
        
        results = []
        for item in search_results[:10]:
            results.append({
                "title": item.get("title", "Без названия"),
                "snippet": item.get("snippet", "").replace("&quot;", '"').replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">"),
                "link": f"https://ru.wikipedia.org/wiki/{quote(item.get('title', ''))}"
            })
        
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Ошибка запроса: {e}")
        return []

def main():
    print("=" * 50)
    print("📚 Парсер Wikipedia (официальное API)")
    print("=" * 50)
    
    print("\nПримеры запросов:")
    print("  • Software testing")
    print("  • Python")
    print("  • Quality assurance")
    print("  • тестирование")
    
    query = input("\n👉 Поисковый запрос (Enter = 'Python'): ").strip()
    if not query:
        query = "Python"
    
    print(f"\n⏳ Ищем '{query}'...\n")
    
    results = search_wikipedia(query)
    
    if results:
        filename = "wikipedia_results.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        
        print(f"\n✅ Сохранено {len(results)} статей в {filename}")
        print("\n📌 Первые 3 результата:")
        for i, r in enumerate(results[:3], 1):
            print(f"\n{i}. {r['title']}")
            print(f"   {r['snippet'][:150]}..." if len(r['snippet']) > 150 else f"   {r['snippet']}")
            print(f"   🔗 {r['link']}")
    else:
        print("\n❌ Статьи не найдены.")
        print("💡 Совет: попробуйте другой запрос или английское слово")

if __name__ == "__main__":
    main()
