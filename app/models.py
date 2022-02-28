
from datetime import time
from unittest import main
from app import db

# TODO дописать класс билета и добавить подпись кассира
# TODO sql скрипт для вставки изначальных данных
# ебучие релайтион шип с back_populates прописываются в двух ебанных классах
# ссылка на ответ умного чеоловека https://coderoad.ru/39869793/Когда-мне-нужно-использовать-sqlalchemy-back_populates

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
    sessions = db.relationship('FilmSession', back_populates='name_film')

    def __init__(self, name: str, id_genre: int,
                 id_author: int, duration) -> None:
        self.name = name
        self.id_genre = id_genre
        self.id_author = id_author
        self.duration = duration


class Genre(db.Model):
    """ 
    TODO docstring
    """
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, comment='Наименование')
    films = db.relationship('Film', back_populates='genre')

    def __init__(self, name: str) -> None:
        self.name = name


class Author(db.Model):
    """ 
    TODO docstring
    """
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, comment='Наименование')
    films = db.relationship('Film', back_populates='author')

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
    tickets = db.relationship('Ticket', back_populates='session_film')


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
    sessions = db.relationship(
        'FilmSession',
        back_populates='cinemahall')


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


class Staff(db.Model):
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
    post = db.Column(
        db.Integer,
        db.ForeignKey('post.id'),
        comment='id дожности'
    )
    tickets = db.relationship('Ticket', back_populates='staff')

    def __init__(self, passport, name, post_id) -> None:
        self.passport = passport
        self.name = name
        self.post = post_id


class Post(db.Model):
    """ 
    Таблица с должностями сотрудников
    """
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, comment='Наименование')
    staff = db.relationship('Staff', back_populates='post')

    def __init__(self, name) -> None:
        self.name = name


def insert_init_data():
    ...
    # должности
    # cashier_post = Post(name='Кассир')
    # db.session.add(cashier_post)
    # db.session.commit()
    # manager_post = Post(name='Менеджер')

    # db.session.add(manager_post)
    # db.session.commit()

    # # сотрудники
    # cashier1 = Staff(
    #     passport='1111123456',
    #     name='Лимонов Вадим Захарович',
    #     post_id=cashier_post.id
    # )

    # cashier2 = Staff(
    #     passport='1112123456',
    #     name='Петров Антон Михайлович',
    #     post_id=cashier_post.id
    # )

    # manager1 = Staff(
    #     passport='1113123456',
    #     name='Борисов Николай Сергеевич',
    #     post_id=manager_post.id
    # )

    # db.session.add(cashier1)
    # db.session.add(cashier2)
    # db.session.add(manager1)
    # db.session.commit()

    # # жанры
    # genre_comedy = Genre(name='Комедия')
    # genre_triller = Genre(name='Триллер')
    # genre_drama = Genre(name='Драма')
    # genre_action = Genre(name='Боевик')
    # genre_tragedy = Genre(name='Трагедия')
    # genre_fantastic = Genre(name='Фантастика')
    # genre_musical = Genre(name='Мюзикл')
    # genre_melodrama = Genre(name='Мелодрама')

    # db.session.add(genre_comedy)
    # db.session.add(genre_triller)
    # db.session.add(genre_drama)
    # db.session.add(genre_action)
    # db.session.add(genre_tragedy)
    # db.session.add(genre_fantastic)
    # db.session.add(genre_musical)
    # db.session.add(genre_melodrama)
    # db.session.commit()

    # # авторы
    # author1 = Author(name='Кислотов Евгений Михайлович')
    # author2 = Author(name='Гаврилов Петр Афанасьевич')
    # author3 = Author(name='Изотов Даниил Андреевич')
    # author4 = Author(name='Петренко Максим Федорович')
    # author5 = Author(name='Левочкин Илья Максимович')
    # author6 = Author(name='Андреева Елизавета Петровна')
    # db.session.add(author1)
    # db.session.add(author2)
    # db.session.add(author3)
    # db.session.add(author4)
    # db.session.add(author5)
    # db.session.add(author6)
    # db.session.commit()

    # # фильмы
    # film1 = Film(
    #     name='Стерва на выданье',
    #     genre_id=genre_drama.id,
    #     author_id=author6.id,
    #     duration=time(1, 20)
    # )
    # film2 = Film(
    #     name='Ачим',
    #     genre_id=genre_fantastic.id,
    #     author_id=author3.id,
    #     duration=time(1, 30)
    # )
    # film3 = Film(
    #     name='Балерина на стене',
    #     genre_id=genre_action.id,
    #     author_id=author1.id,
    #     duration=time(1, 40)
    # )
    # film4 = Film(
    #     name='Собаки в чемодане',
    #     genre_id=genre_triller.id,
    #     author_id=author2.id,
    #     duration=time(1, 350)
    # )
    # db.session.add(film1)
    # db.session.add(film2)
    # db.session.add(film3)
    # db.session.add(film4)
    # db.session.commit()


insert_init_data()
