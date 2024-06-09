from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


class Base:
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def execute_data(cls, query: str):
        result = db.session.execute(text(query))
        return result.fetchall()


class User(db.Model, Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return (f'id:{self.id},name:{self.name},email:{self.email}')

    @classmethod
    def find_by_email(cls, email: str) -> 'User':
        return cls.query.filter_by(email=email).first()


class Score(db.Model, Base):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    point_snake = db.Column(db.Integer, nullable=False, default=0)
    point_bricks = db.Column(db.Integer, nullable=False, default=0)
    point_tetris = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return (f'id:{self.id}, point_snake:{self.point_snake}, point_bricks:{self.point_bricks}, '
                f'point_tetris:{self.point_tetris}, user_id:{self.user_id}')


def get_rating():
    query = Base.execute_data("""
    SELECT users.name, (scores.point_snake + scores.point_bricks + scores.point_tetris) as total_point
    FROM users
    join scores on scores.user_id = users.id
    order by total_point desc
    """)
    return query
