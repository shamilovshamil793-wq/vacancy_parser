# Парсеры данных на Python

Два работающих парсера для сбора данных из публичных API.

## Проекты

### 1. Парсер JSONPlaceholder API (`parser_api.py`)
- Получает данные из тестового REST API
- Поддерживает: посты, комментарии, задачи
- Сохраняет результат в JSON

### 2. Парсер Wikipedia API (`parser_wiki.py`)
- Ищет статьи по ключевым словам
- Работает с русской Wikipedia
- Получает: заголовок, сниппет, ссылку

## Технологии
- Python 3
- requests
- JSON

## Запуск

```bash
pip install requests
python parser_api.py
python parser_wiki.py
cat >> README.md << 'EOF'

## Автор
[Шамил Шамилов]

## Ссылка на репозиторий
https://github.com/shamilovshamil793-wq/vacancy_parser
