import sys
sys.path.append('../')
from app import db
from app.models import *
from datetime import time 
def insert_init_data():
    session = db.session
    # должности
    cashier_post = Post(name='Кассир')
    manager_post = Post(name='Менеджер')

    session.add(cashier_post)
    session.add(manager_post)
    session.commit()

    # сотрудники
    cashier1 = Staff(
        passport='1111123456',
        name='Лимонов Вадим Захарович',
        post_id=cashier_post.id
    )

    cashier2 = Staff(
        passport='1112123456',
        name='Петров Антон Михайлович',
        post_id=cashier_post.id
    )

    manager1 = Staff(
        passport='1113123456',
        name='Борисов Николай Сергеевич',
        post_id=manager_post.id
    )

    session.add(cashier1)
    session.add(cashier2)
    session.add(manager1)
    session.commit()

    # жанры
    genre_comedy = Genre(name='Комедия')
    genre_triller = Genre(name='Триллер')
    genre_drama = Genre(name='Драма')
    genre_action = Genre(name='Боевик')
    genre_tragedy = Genre(name='Трагедия')
    genre_fantastic = Genre(name='Фантастика')
    genre_musical = Genre(name='Мюзикл')
    genre_melodrama = Genre(name='Мелодрама')

    session.add(genre_comedy)
    session.add(genre_triller)
    session.add(genre_drama)
    session.add(genre_action)
    session.add(genre_tragedy)
    session.add(genre_fantastic)
    session.add(genre_musical)
    session.add(genre_melodrama)
    session.commit()

    # авторы
    author1 = Author(name='Кислотов Евгений Михайлович')
    author2 = Author(name='Гаврилов Петр Афанасьевич')
    author3 = Author(name='Изотов Даниил Андреевич')
    author4 = Author(name='Петренко Максим Федорович')
    author5 = Author(name='Левочкин Илья Максимович')
    author6 = Author(name='Андреева Елизавета Петровна')
    session.add(author1)
    session.add(author2)
    session.add(author3)
    session.add(author4)
    session.add(author5)
    session.add(author6)
    session.commit()

    # фильмы
    film1 = Film(
        name='Стерва на выданье',
        genre_id=genre_drama.id,
        author_id=author6.id,
        duration=time(1, 20)
    )
    film2 = Film(
        name='Ачим',
        genre_id=genre_fantastic.id,
        author_id=author3.id,
        duration=time(1, 30)
    )
    film3 = Film(
        name='Балерина на стене',
        genre_id=genre_action.id,
        author_id=author1.id,
        duration=time(1, 40)
    )
    film4 = Film(
        name='Собаки в чемодане',
        genre_id=genre_triller.id,
        author_id=author2.id,
        duration=time(1, 350)
    )
    session.add(film1)
    session.add(film2)
    session.add(film3)
    session.add(film4)
    session.commit()


if __name__ == 'main':
    insert_init_data()
