import os
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from database import Session, DatabaseManager
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()


def fetch_and_store_problems():
    url = 'https://codeforces.com/api/problemset.problems'
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        problems = data['result']['problems']
        problem_stats = data['result']['problemStatistics']

        session = Session()
        db_manager = DatabaseManager(session)

        # Создание словаря для хранения solved_count
        solved_count_dict = {}
        for stat in problem_stats:
            key = (stat['contestId'], stat['index'])
            solved_count_dict[key] = stat['solvedCount']

        for problem in problems:
            key = (problem['contestId'], problem['index'])
            problem_data = {
                'contest_id': problem['contestId'],
                'index': problem['index'],
                'name': problem['name'],
                'type': problem['type'],
                'rating': problem.get('rating', 0),
                'solved_count': solved_count_dict.get(key, 0),
                'tags': problem.get('tags', [])
            }
            db_manager.add_problem(problem_data)

        session.close()


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(fetch_and_store_problems, 'interval', hours=1)
    print("Starting scheduler...")
    fetch_and_store_problems()  # Запуск парсинга при старте
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
