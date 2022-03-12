from datetime import datetime, time
from time import sleep
from flask import render_template, request, url_for, redirect, g, flash
from flask_login import login_user, logout_user, current_user
from app import app, db, bc, lm
from app.models import Cinemahall, FilmView, Staff, StaffView, Genre, Author, Film, Post
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
    return render_template('author/delete_author.html', name=del_name)


@app.route('/films', methods=['GET', 'POST'])
def view_films():
    """Функция для отображения всех фильмов"""
    films = FilmView.query.all()
    return render_template('film/film.html', data=films, Film=FilmView)


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
        if film and film.name != film_change.name:
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


@app.route('/staff', methods=['GET', 'POST'])
def view_staff():
    """Функция для отображения сотрудников"""
    staff = StaffView.query.all()
    print(staff)
    return render_template('staff/staff.html', data=staff, Staff=StaffView)


@app.route('/staff/add', methods=['GET', 'POST'])
def add_staff():
    """Функция для добавления нового сотрудника"""
    form = StaffForm()
    form.post.choices = [(g.id, g.name)
                         for g in Post.query.order_by('name')]
    if form.validate_on_submit():
        passport = request.form.get('passport', '', type=str)
        name = request.form.get('name', '', type=str)
        post_id = request.form.get('post', '', type=int)
        login = request.form.get('login', '', type=str)
        password = request.form.get('password', '', type=str)

        staff: Staff = Staff.query.filter_by(passport=passport).first()
        if staff:
            flash('Данный сотрудник уже есть в БД! Данные не записаны')
        else:
            new_staff = Staff(
                passport=passport,
                name=name,
                post_id=post_id,
                login=login,
                password=password
            )
            db.session.add(new_staff)
            db.session.commit()
            flash('Сотрудник успешно добавлен!')
    return render_template('staff/add_staff.html', form=form)


@app.route('/staff/edit/<string:passport>', methods=['GET', 'POST'])
def edit_staff(passport: str):
    """Функция для редактирования сотрудника"""
    staff_change: Staff = Staff.query.filter_by(passport=passport).first()
    form = StaffForm()
    # ставим в форму предыдущие значения элемента
    form.name.default = staff_change.name
    form.post.choices = [(g.id, g.name)
                         for g in Post.query.order_by('name')]
    form.post.default = staff_change.post_id

    form.login.default = staff_change.login
    form.passport.default = staff_change.passport
    form.password.default = staff_change.password

    form.submit.label.text = 'Изменить'
    # обработка формы, без этого значения не подставятся
    form.process()

    if form.validate_on_submit():
        passport = request.form.get('passport', '', type=str)
        name = request.form.get('name', '', type=str)
        post_id = request.form.get('post', '', type=int)
        login = request.form.get('login', '', type=str)
        password = request.form.get('password', '', type=str)

        staff: Staff = Staff.query.filter_by(passport=passport).first()
        if staff and staff.passport != staff_change.passport:
            flash('Данный сотрудник уже есть в БД! Данные не записаны')
        else:
            staff_change.name = name
            staff_change.post_id = post_id
            staff_change.login = login
            staff_change.password = password
            staff_change.passport = passport
            db.session.add(staff_change)
            db.session.commit()
            flash('Сотрудник успешно изменен!')
    return render_template('staff/edit_staff.html', form=form)


@app.route('/staff/delete/<string:passport>', methods=['GET', 'POST'])
def delete_staff(passport: str):
    """Функция для удаления сотрудника по id

    :param passport: серия и номер паспорта сотрудника
    """
    del_staff = Staff.query.filter_by(passport=passport).first()
    del_name = f'{del_staff.name} ({del_staff.passport})'
    db.session.delete(del_staff)
    db.session.commit()
    return render_template('staff/delete_staff.html', name=del_name)


@app.route('/cinemahall', methods=['GET', 'POST'])
def view_cinemahall():
    cinemahalls = Cinemahall.query.all()
    return render_template('cinemahall/cinemahall.html', data=cinemahalls, Cinemahall=Cinemahall)


@app.route('/cinemahall/add', methods=['GET', 'POST'])
def add_cinemahall():
    form = CinemahallForm()
    if form.validate_on_submit():
        name = request.form.get('name', '', type=str)
        capacity = request.form.get('capacity', '', type=str)
        cinemahall: Cinemahall = Cinemahall.query.filter_by(name=name).first()
        if cinemahall:
            flash('Данный кинозал уже есть в БД! Данные не записаны')
        else:
            cinemahall = Cinemahall(
                name=name,
                capacity=capacity
            )
            db.session.add(cinemahall)
            db.session.commit()
            flash('Кинозал успешно добавлен!')
    return render_template('cinemahall/add_cinemahall.html', form=form)


@app.route('/cinemahall/edit/<int:cinemahall_id>', methods=['GET', 'POST'])
def edit_cinemahall(cinemahall_id: int):
    """Функция для редактирования кинозала"""
    cinemahall_change: Cinemahall = Cinemahall.query.filter_by(
        id=cinemahall_id).first()
    form = CinemahallForm()
    form.name.default = cinemahall_change.name
    form.capacity.default = cinemahall_change.capacity
    form.submit.label.text = 'Изменить'

    form.process()

    if form.validate_on_submit():
        name = request.form.get('name', '', type=str)
        capacity = request.form.get('capacity', '', type=int)
        cinemahall = Cinemahall.query.filter_by(name=name).first()
        if cinemahall:
            flash('Данный кинозал уже есть в БД! Данные не записаны')
        else:
            cinemahall_change.name = name
            cinemahall_change.capacity = capacity
            db.session.add(cinemahall_change)
            db.session.commit()
            flash('Кинозал успешно изменен!')
    return render_template('cinemahall/edit_cinemahall.html', form=form)


@app.route('/cinemahall/delete/<int:cinemahall_id>', methods=['GET', 'POST'])
def delete_cinemahall(cinemahall_id: str):
    """Функция для удаления кинозала по id

    :param cinemahall_id: id сотрудника
    """
    delete_cinemahall: Cinemahall = Cinemahall.query.filter_by(
        id=cinemahall_id).first()
    del_name = delete_cinemahall.name
    db.session.delete(delete_cinemahall)
    db.session.commit()
    return render_template('cinemahall/delete_cinemahall.html', name=del_name)


@app.before_request
def before_request():
    g.user = current_user


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('login'))

    return response
