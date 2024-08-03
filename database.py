import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

Base = declarative_base()

problem_tag_table = Table('problem_tag', Base.metadata,
                          Column('problem_id', Integer, ForeignKey('problems.id'), primary_key=True),
                          Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
                          )


class Problem(Base):
    __tablename__ = 'problems'
    id = Column(Integer, primary_key=True)
    contest_id = Column(Integer)
    index = Column(String)
    name = Column(String)
    type = Column(String)
    rating = Column(Integer)
    solved_count = Column(Integer, default=0)
    tags = relationship('Tag', secondary=problem_tag_table, back_populates='problems')


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    problems = relationship('Problem', secondary=problem_tag_table, back_populates='tags')


DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class DatabaseManager:
    def __init__(self, session):
        self.session = session

    def add_problem(self, problem_data):
        problem = self.session.query(Problem).filter_by(contest_id=problem_data['contest_id'],
                                                        index=problem_data['index']).first()
        if not problem:
            problem = Problem(
                contest_id=problem_data['contest_id'],
                index=problem_data['index'],
                name=problem_data['name'],
                type=problem_data['type'],
                rating=problem_data['rating'],
                solved_count=problem_data.get('solved_count', 0)
            )
            self.session.add(problem)
            self.session.commit()

        for tag_name in problem_data['tags']:
            tag = self.session.query(Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                self.session.add(tag)
                self.session.commit()
            if tag not in problem.tags:
                problem.tags.append(tag)
        self.session.commit()

    def update_solved_count(self, contest_id, index, solved_count):
        problem = self.session.query(Problem).filter_by(contest_id=contest_id, index=index).first()
        if problem:
            problem.solved_count = solved_count
            self.session.commit()
