import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Problem, Tag, DatabaseManager

DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope='module')
def engine():
    return create_engine(DATABASE_URL)


@pytest.fixture(scope='module')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function')
def session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session
    session.close()
    transaction.rollback()
    connection.close()


def test_database(session):
    db_manager = DatabaseManager(session)
    problem_data = {
        'contest_id': 1001,
        'index': 'A',
        'name': 'Sample Problem',
        'type': 'PROGRAMMING',
        'rating': 1200,
        'tags': ['math', 'implementation'],
        'solved_count': 10
    }

    db_manager.add_problem(problem_data)

    problem = session.query(Problem).filter_by(contest_id=1001, index='A').first()
    assert problem is not None
    assert problem.name == 'Sample Problem'
    assert problem.rating == 1200
    assert problem.solved_count == 10
    assert len(problem.tags) == 2
    assert problem.tags[0].name == 'math'
    assert problem.tags[1].name == 'implementation'
