from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TimeField, IntegerField
from wtforms.validators import DataRequired


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
    Форма для редактирования жанра в справочнике
    """
    name = StringField(label='Новое наименование:',
                       validators=[DataRequired('Данное поле обязательно')],
                       render_kw={'placeholder': 'Введите наименование жанра'})
    submit = SubmitField('Изменить')


class AddAuthorForm(FlaskForm):
    """
    Форма для добавления нового автора в справочник
    """
    name = StringField(label='ФИО:',
                       validators=[DataRequired('Данное поле обязательно')],
                       render_kw={'placeholder': 'Введите ФИО автора'})
    submit = SubmitField('Записать')


class EditAuthorForm(FlaskForm):
    """
    Форма для редактирования автора в справочнике
    """
    name = StringField(label='Новое ФИО:',
                       validators=[DataRequired('Данное поле обязательно')],
                       render_kw={'placeholder': 'Введите ФИО автора'})
    submit = SubmitField('Изменить')


class AddFilmForm(FlaskForm):
    """
    Форма для добавления нового фильма
    """
    name = StringField(label='Название фильма:',
                       validators=[DataRequired('Данное поле обязательно')],
                       render_kw={'placeholder': 'Введите название фильма'})
    genre = SelectField(u'Жанр', coerce=int)
    author = SelectField(u'Автор', coerce=int)
    duration = TimeField('Продолжительность',
                         validators=[DataRequired('Данное поле обязательно')],
                         render_kw={'placeholder': 'Введите продолжительность фильма'})
    submit = SubmitField('Записать')


class EditFilmForm(FlaskForm):
    """
    Форма для редактирования фильма
    """
    name = StringField(label='Название фильма:',
                       validators=[DataRequired('Данное поле обязательно')],
                       render_kw={'placeholder': 'Введите название фильма'})
    genre = SelectField(u'Жанр', coerce=int)
    author = SelectField(u'Автор', coerce=int)
    duration = TimeField('Продолжительность',
                         validators=[DataRequired('Данное поле обязательно')],
                         render_kw={'placeholder': 'Введите продолжительность фильма'})
    submit = SubmitField('Изменить')


class StaffForm(FlaskForm):
    """ 
    Форма для добавления/изменения сотрудника
    """
    passport = StringField(label='Серия и номер паспорта:',
                           validators=[DataRequired(
                               'Данное поле обязательно')],
                           render_kw={'placeholder': 'Введите данные'})
    name = StringField(label='ФИО:',
                       validators=[DataRequired('Данное поле обязательно')],
                       render_kw={'placeholder': 'Введите ФИО'})
    post = SelectField(u'Должность', coerce=int)
    login = StringField(label='Логин:',
                        validators=[DataRequired('Данное поле обязательно')],
                        render_kw={'placeholder': 'Введите логин'})
    password = StringField(label='Пароль:',
                           validators=[DataRequired(
                               'Данное поле обязательно')],
                           render_kw={'placeholder': 'Введите пароль'})
    submit = SubmitField('Записать')


class CinemahallForm(FlaskForm):
    """ 
    Форма для добавления/изменения кинозала
    """
    name = StringField(label='Наименование:',
                       validators=[DataRequired('Данное поле обязательно')],
                       render_kw={'placeholder': 'Введите наименование'})
    capacity = IntegerField(label='Вместимость:',
                            validators=[DataRequired(
                                'Данное поле обязательно')],
                            render_kw={'placeholder': 'Введите вместимость'})
    submit = SubmitField('Записать')
