import dataclasses
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from config import *

db = SQLAlchemy()

def setup_db(app, database_path=SQLALCHEMY_DATABASE_URI):
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    db.app = app
    db.init_app(app)

    with app.app_context():
        db.create_all()

class BaseModel(db.Model):
    __abstract__ = True

    def insert(self):
       db.session.add(self)
       db.session.commit()

    def delete(self):
       db.session.delete(self)
       db.session.commit()

    def update(self):
       db.session.commit()

@dataclasses
class Movie(BaseModel):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    @property
    def movies_count(self):
      movies_list = Movie.query.all()
      return len(movies_list)

@dataclasses
class Actor(BaseModel):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(30), nullable=False)

    @property
    def actors_count(self):
      actors_list = Actor.query.all()
      return len(actors_list)
