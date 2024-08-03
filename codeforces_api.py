import requests


class CodeforcesAPI:
    BASE_URL = "https://codeforces.com/api/"

    def fetch_problems(self):
        url = self.BASE_URL + "problemset.problems"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                problems = data['result']['problems']
                statistics = data['result']['problemStatistics']
                return self._merge_data(problems, statistics)
        return []

    def _merge_data(self, problems, statistics):
        stats_map = {stat['contestId']: stat for stat in statistics}
        merged = []
        for problem in problems:
            contest_id = problem.get('contestId', 0)
            index = problem.get('index', '')
            stat = stats_map.get(contest_id, {})
            problem_data = {
                'name': problem['name'],
                'problem_id': f"{contest_id}{index}",
                'contest_id': contest_id,
                'points': problem.get('points', 0.0),
                'rating': problem.get('rating', None),
                'tags': problem.get('tags', []),
                'solved_count': stat.get('solvedCount', 0)
            }
            merged.append(problem_data)
        return merged
