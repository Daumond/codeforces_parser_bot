import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Problem, Tag, DatabaseManager

# Use a different database for testing
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


@pytest.fixture
def session():
    return Session()


def test_database(session):
    db_manager = DatabaseManager(session)
    problem_data = {
        'name': 'Example Problem',
        'problem_id': '1234A',
        'contest_id': 1234,
        'points': 1000,
        'rating': 800,
        'tags': ['math'],
        'solved_count': 100
    }
    db_manager.add_problem(problem_data)

    problem = session.query(Problem).filter_by(problem_id='1234A').first()
    assert problem is not None
    assert problem.name == 'Example Problem'
    assert problem.rating == 800
    assert problem.solved_count == 100
    assert len(problem.tags) == 1
    assert problem.tags[0].name == 'math'
