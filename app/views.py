from datetime import datetime, time
from time import sleep
from flask import render_template, request, url_for, redirect, g, flash
from flask_login import login_user, logout_user, current_user
from app import app, db, bc, lm
from app.models import Staff, Genre, Author, Film
from app.forms import *
# TODO переписать на классы


@lm.user_loader
def load_user(user_id):
    return Staff.query.get(str(login))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm(request.form)

    if form.validate_on_submit():
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str)

        user = Staff.query.filter_by(login=username).first()

        if user:
            if user.password == password:  # да-да, шифрование по пизде и нихера не безопасно, но мне ПОХУЙ
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Неверный пароль. Проверьте правильность введеных данных.')
        else:
            flash("Неизвестный пользователь.")

    return render_template('login.html', form=form)


@app.route('/')
def index():
    """Функция для отображения начальной страницы"""
    return render_template('index.html')


@app.route('/genres')
def view_genres():
    """Функция для отображения всех жанров"""
    genres = Genre.query.order_by(Genre.id.asc()).all()
    return render_template('genre/genre.html', data=genres, Genre=Genre)


@app.route('/genres/add', methods=['GET', 'POST'])
def add_genres():
    """Функция для добавления жанров"""
    form = AddGenreForm()
    if form.validate_on_submit():
        genre_name = request.form.get('name', '', type=str)
        genre = Genre.query.filter_by(name=genre_name).first()
        if genre:
            flash('Данный жанр уже есть в БД! Данные не записаны')
        else:
            new_genre = Genre(name=genre_name)
            db.session.add(new_genre)
            db.session.commit()
            flash('Жанр успешно добавлен!')
    return render_template('genre/add_genre.html', form=form)


@app.route('/genres/edit/<int:genre_id>', methods=['GET', 'POST'])
def edit_genre(genre_id: int):
    """Функция для редактирования жанров"""
    genre_change = Genre.query.filter_by(id=genre_id).first()
    form = EditGenreForm()
    if form.validate_on_submit():
        genre_name = request.form.get('name', '', type=str)
        genre = Genre.query.filter_by(name=genre_name).first()
        if genre:
            flash('Данный жанр уже есть в БД! Данные не записаны')
        else:
            genre_change.name = genre_name
            db.session.add(genre_change)
            db.session.commit()
            flash('Жанр успешно изменен!')
    return render_template('genre/edit_genre.html', form=form, old_name=genre_change.name)


@app.route('/genres/delete/<int:genre_id>', methods=['GET', 'POST'])
def delete_genre(genre_id: int):
    """Функция для удаления жанров"""
    del_genre = Genre.query.filter_by(id=genre_id).first()
    del_name = del_genre.name
    db.session.delete(del_genre)
    db.session.commit()
    return render_template('genre/delete_genre.html', name=del_name)


@app.route('/authors')
def view_authors():
    """Функция для отображения всех авторов"""
    authors = Author.query.order_by(Author.id.asc()).all()
    return render_template('author/author.html', data=authors, Author=Author)


@app.route('/authors/add', methods=['GET', 'POST'])
def add_authors():
    """Функция для добавления авторов"""
    form = AddAuthorForm()
    if form.validate_on_submit():
        author_name = request.form.get('name', '', type=str)
        author = Author.query.filter_by(name=author_name).first()
        if author:
            flash('Данный автор уже есть в БД! Данные не записаны')
        else:
            new_author = Author(name=author_name)
            db.session.add(new_author)
            db.session.commit()
            flash('Автор успешно добавлен!')
    return render_template('author/add_author.html', form=form)


@app.route('/authors/edit/<int:author_id>', methods=['GET', 'POST'])
def edit_author(author_id: int):
    """Функция для редактирования авторов"""
    author_change = Author.query.filter_by(id=author_id).first()
    form = EditAuthorForm()
    if form.validate_on_submit():
        author_name = request.form.get('name', '', type=str)
        author = Author.query.filter_by(name=author_name).first()
        if author:
            flash('Данный автор уже есть в БД! Данные не записаны')
        else:
            author_change.name = author_name
            db.session.add(author_change)
            db.session.commit()
            flash('Автор успешно изменен!')
    return render_template('author/edit_author.html', form=form, old_name=author_change.name)


@app.route('/authors/delete/<int:author_id>', methods=['GET', 'POST'])
def delete_author(author_id: int):
    del_author = Author.query.filter_by(id=author_id).first()
    del_name = del_author.name
    db.session.delete(del_author)
    db.session.commit()
    return render_template('authors/delete_author.html', name=del_name)


@app.route('/films', methods=['GET', 'POST'])
def view_films():
    """Функция для отображения всех фильмов"""
    films = Film.query.order_by(
        Film.id.asc()).all()  # TODO правильное отображение
    films = Film.query\
        .join(
            Genre, Film.id_genre == Genre.id
        ).join(
            Author, Film.id_author == Author.id
        ).with_entities(Film.id, Film.name, Genre.name, Author.name, Film.duration).all()
    films_dict = {}
    for film in films:
        films_dict[film[0]] = {
            "name": film[1],
            "genre": film[2],
            "author":film[3],
            "duration":film[4]
        }
    return render_template('film/film.html', data=films_dict, Film=Film)


@app.route('/films/edit/<int:film_id>', methods=['GET', 'POST'])
def edit_film(film_id: int):
    """Функция для редактирования фильмов"""
    film_change: Film = Film.query.filter_by(id=film_id).first()
    form = EditFilmForm()
    # ставим в форму предыдущие значения элемента
    form.name.default = film_change.name
    form.genre.choices = [(g.id, g.name)
                          for g in Genre.query.order_by('name')]
    form.genre.default = film_change.id_genre
    form.author.choices = [(g.id, g.name)
                           for g in Author.query.order_by('name')]
    form.author.default = film_change.id_author
    form.duration.default = film_change.duration
    # обработка формы, без этого значения не подставятся
    form.process()
    if form.validate_on_submit():
        film_name = request.form.get('name', '', type=str)
        genre_id = request.form.get('genre', '', type=int)
        author_id = request.form.get('author', '', type=int)
        duration = request.form.get('duration', '', type=time)
        film = Film.query.filter_by(name=film_name).first()
        if film:
            flash('Данный фильм уже есть в БД! Данные не записаны')
        else:
            film_change.name = film_name
            film_change.id_author = author_id
            film_change.id_genre = genre_id
            film_change.duration = duration
            db.session.add(film_change)
            db.session.commit()
            flash('Фильм успешно изменен!')
    return render_template('film/edit_film.html', form=form, old_name=film_change.name)


@app.route('/films/delete/<int:film_id>', methods=['GET', 'POST'])
def delete_film(film_id: int):
    """Функция для удаления фильма по id

    :param film_id: id фильма
    """
    del_film = Film.query.filter_by(id=film_id).first()
    del_name = del_film.name
    db.session.delete(del_film)
    db.session.commit()
    return render_template('authors/delete_author.html', name=del_name)


@app.route('/films/add', methods=['GET', 'POST'])
def add_film():
    form = AddFilmForm()
    form.genre.choices = [(g.id, g.name)
                          for g in Genre.query.order_by('name')]
    form.author.choices = [(g.id, g.name)
                           for g in Author.query.order_by('name')]
    if form.validate_on_submit():
        film_name = request.form.get('name', '', type=str)
        genre_id = request.form.get('genre', '', type=int)
        author_id = request.form.get('author', '', type=int)
        duration = request.form.get('duration', '', type=time)

        film = Film.query.filter_by(name=film_name).first()
        if film:
            flash('Данный фильм уже есть в БД! Данные не записаны')
        else:
            new_film = Film(name=film_name, id_genre=genre_id,
                            id_author=author_id)
            db.session.add(new_film)
            db.session.commit()
            flash('Фильм успешно добавлен!')
    return render_template('film/add_film.html', form=form)


@app.before_request
def before_request():
    g.user = current_user


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('login'))

    return response
