from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from app.models import Genre


# TODO проверка всех значений в формах
class LoginForm(FlaskForm):
    """
    Форма для авторизации пользователей
    """
    username = StringField(label='Логин:',
                           validators=[DataRequired(
                               'Данное поле обязательно')],
                           render_kw={'placeholder': 'Введите логин'})
    password = PasswordField('Пароль:',
                             validators=[DataRequired(
                                 'Данное поле обязательно')],
                             render_kw={'placeholder': 'Введите пароль'})
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')


class AddGenreForm(FlaskForm):
    """
    Форма для добавления нового жанра в справочник
    """
    name = StringField(label='Наименование:',
                       validators=[DataRequired('Данное поле обязательно')],
                       render_kw={'placeholder': 'Введите наименование жанра'})
    submit = SubmitField('Записать')


class EditGenreForm(FlaskForm):
    """
    Форма для добавления нового жанра в справочник
    """
    name = StringField(label='Новое наименование:',
                       validators=[DataRequired('Данное поле обязательно')],
                       render_kw={'placeholder': 'Введите наименование жанра'})
    submit = SubmitField('Изменить')
