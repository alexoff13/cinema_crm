from time import sleep
from flask import render_template, request, url_for, redirect, g, flash
from flask_login import login_user, logout_user, current_user
from app import app, db, bc, lm
from app.models import Staff, Genre
from app.forms import LoginForm, AddGenreForm, EditGenreForm


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
    return render_template('genre.html', data=genres, Genre=Genre)


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
    return render_template('add_genre.html', form=form)


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
            sleep(1)
            redirect('/genres')
    return render_template('edit_genre.html', form=form, old_name=genre_change.name)


@app.route('/genres/delete/<int:genre_id>', methods=['GET', 'POST'])
def delete_genre(genre_id: int):
    del_genre = Genre.query.filter_by(id=genre_id).first()
    del_name = del_genre.name
    db.session.delete(del_genre)
    db.session.commit()
    return render_template('delete_genre.html', name=del_name)

 
@app.before_request
def before_request():
    g.user = current_user


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('login'))

    return response
