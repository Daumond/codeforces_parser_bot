import pytest
from codeforces_api import CodeforcesAPI


def test_fetch_problems():
    api = CodeforcesAPI()
    problems = api.fetch_problems()
    assert len(problems) > 0
    for problem in problems:
        assert 'name' in problem
        assert 'problem_id' in problem
        assert 'solved_count' in problem
        assert 'rating' in problem
