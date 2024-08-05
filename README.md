# Codeforces Problem Parser and Telegram Bot

## Описание

Проект предназначен для парсинга задач с сайта Codeforces, сохранения их в базу данных и предоставления возможности поиска задач через Telegram-бота.

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/your-repo/codeforces-parser-bot.git
    cd codeforces-parser-bot
    ```

2. Создайте файл `.env` из `sample.env` и заполните его 



3. Запустите проект с помощью Docker:

    ```bash
    docker-compose up --build
    ```

## Использование

1. Запустите скрипт для парсинга задач:

    ```bash
    docker-compose run --rm app python codeforces_parser.py
    ```

2. Запустите Telegram-бота:

    ```bash
    docker-compose run --rm app python bot.py
    ```

## Пример запроса и ответа Telegram-бота

- **Запрос:**

    ```plaintext
    /find
    ```

- **Ответ:**

    ```plaintext
    Привет! Выберите сложность задачи (например, 800, 1200 и т.д.):
    ```

- **Запрос:**

    ```plaintext
    1200
    ```

- **Ответ:**

    ```plaintext
    Выберите тему задачи (например, 'math', 'dp' и т.д.):
    ```

- **Запрос:**

    ```plaintext
    math
    ```

- **Ответ:**

    ```plaintext
    Вот задачи, соответствующие вашему запросу:
    Название: Sample Problem
    Сложность: 1200
    Количество решений: 10
    Ссылка: https://codeforces.com/contest/1001/problem/A
    ```

## Тестирование

Запустите тесты с помощью pytest:

```bash
docker-compose run --rm app pytest
```