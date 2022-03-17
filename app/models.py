
from datetime import time
from zoneinfo import available_timezones
from app import db
from flask_login import UserMixin


class Film(db.Model):
    """ 
    TODO docstring
    """
    __tablename__ = 'film'
    __table_args__ = (
        # для использования в качестве foreign_key
        #  (nullable=False тоже для этого)
        db.UniqueConstraint('name'),
    )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, comment='Название')
    id_genre = db.Column(
        db.Integer,
        db.ForeignKey('genre.id'),
        comment='id жанра'
    )
    id_author = db.Column(
        db.Integer,
        db.ForeignKey('author.id'),
        comment='id режиссера'
    )
    duration = db.Column(db.Time, comment='Продолжительность')
    # sessions = db.relationship('FilmSession', back_populates='film')
    # genre = db.relationship('Genre', back_populates='films', uselist=False)
    # author = db.relationship('Author', back_populates='films', uselist=False)

    def __init__(self, name: str, id_genre: int,
                 id_author: int, duration) -> None:
        self.name = name
        self.id_genre = id_genre
        self.id_author = id_author
        self.duration = duration


class FilmView(db.Model):
    """ 
    Класс для маппинга представления фильмов из БД.
    DDL содержится в переменной __ddl
    """
    __tablename__ = 'film_view'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genre_name = db.Column(db.String)
    author_name = db.Column(db.String)
    duration = db.Column(db.Time)

    __ddl = """
    CREATE OR REPLACE VIEW public.film_view
    AS SELECT f.id,
        f.name,
        g.name AS genre_name,
        a.name AS author_name,
        f.duration
   FROM film f
        JOIN genre g ON g.id = f.id_genre
        JOIN author a ON a.id = f.id_author;
    """


class Genre(db.Model):
    """ 
    TODO docstring
    """
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, comment='Наименование')
    # films = db.relationship('Film', back_populates='genre')

    def __init__(self, name: str) -> None:
        self.name = name


class Author(db.Model):
    """ 
    TODO docstring
    """
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, comment='Наименование')
    # films = db.relationship('Film', back_populates='author')

    def __init__(self, name: str) -> None:
        self.name = name


class FilmSession(db.Model):
    """ 
    TODO docstring
    """
    __tablename__ = 'session_film'
    __table_args__ = (
        # для использования в качестве foreign_key
        #  (nullable=False тоже для этого)
        db.UniqueConstraint('date_time', 'name_cinemahall'),
    )
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(
        db.DateTime,
        comment='Дата и время сеанса'
    )
    name_film = db.Column(
        db.String,
        db.ForeignKey('film.name'),
        comment='Название фильма'
    )
    name_cinemahall = db.Column(
        db.String,
        db.ForeignKey('cinemahall.name'),
        comment='Наименование кинозала'
    )


class SheduleSession(db.Model):
    """ 
    Таблица с расписанием фильмов (для кассиров и покупателей)
    """
    __tablename__ = 'film_session_view'
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime)
    name_film = db.Column(db.String)
    name_cinemahall = db.Column(db.String)
    available_tickets = db.Column(db.Integer)


class Cinemahall(db.Model):
    """ 
    TODO docstring
    """
    __tablename__ = 'cinemahall'
    __table_args__ = (
        # для использования в качестве foreign_key
        #  (nullable=False тоже для этого)
        db.UniqueConstraint('name'),
    )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String,
        nullable=False,
        comment='Название'
    )
    capacity = db.Column(db.Integer, comment='Вместимость')

    def __init__(self, name: str, capacity: int) -> None:
        self.name = name
        self.capacity = capacity


class Ticket(db.Model):
    """ 
    Таблица с билетами на сеанс
    """
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    id_session = db.Column(
        db.Integer,
        db.ForeignKey('session_film.id'),
        comment='id сеанса'
    )
    signature_cashier = db.Column(
        db.String,
        db.ForeignKey('staff.passport'),
        comment='Подпись кассира'
    )

    def __init__(self, id_session, signature_cashier) -> None:
        self.id_session = id_session
        self.signature_cashier = signature_cashier


class CashierTicket(db.Model):
    __tablename__ = 'cashier_ticket'
    passport = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    count_sell = db.Column(db.Integer)


class Staff(UserMixin, db.Model):
    """ 
    Таблица с сотрудниками
    """
    __tablename__ = 'staff'
    passport = db.Column(
        db.String,
        primary_key=True,
        comment='Серия и номер паспорта'
    )
    name = db.Column(db.String, comment='ФИО')
    login = db.Column(db.String)
    password = db.Column(db.String)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('post.id'),
        comment='id дожности'
    )

    def __init__(self, passport, name, post_id, login, password) -> None:
        self.passport = passport
        self.name = name
        self.post_id = post_id
        self.login = login
        self.password = password

    def get_id(self):
        return int(self.passport)


class StaffView(db.Model):
    __tablename__ = 'staff_view'

    passport = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    login = db.Column(db.String)
    password = db.Column(db.String)
    post = db.Column(db.String)


class Post(db.Model):
    """ 
    Таблица с должностями сотрудников
    """
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, comment='Наименование')

    def __init__(self, name) -> None:
        self.name = name
