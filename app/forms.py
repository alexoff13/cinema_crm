from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TimeField, IntegerField, DateTimeLocalField
from wtforms.validators import DataRequired, Regexp, NumberRange


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
                       validators=[
                           DataRequired('Данное поле обязательно'),
                           Regexp(regex=r'\A[А-Я][а-я][а-я]*\Z',
                                  message='Формат: с большой буквы, >2 символов')
                       ],
                       render_kw={'placeholder': 'Введите наименование жанра'})
    submit = SubmitField('Записать')


class EditGenreForm(FlaskForm):
    """
    Форма для редактирования жанра в справочнике
    """
    name = StringField(label='Новое наименование:',
                       validators=[
                           DataRequired('Данное поле обязательно'),
                           Regexp(regex=r'\A[А-Я][а-я][а-я]*\Z',
                                  message='Формат: с большой буквы, >2 символов')
                       ],
                       render_kw={'placeholder': 'Введите наименование жанра'})
    submit = SubmitField('Изменить')


class AddAuthorForm(FlaskForm):
    """
    Форма для добавления нового автора в справочник
    """
    name = StringField(label='ФИО:',
                       validators=[
                           DataRequired('Данное поле обязательно'),
                           Regexp(regex=r'\A[А-Яа-я ]*\Z',
                                  message='Формат: Фамилия Имя Отчество, >2 символов в каждой части ФИО')
                       ],
                       render_kw={'placeholder': 'Введите ФИО автора'})
    submit = SubmitField('Записать')


class EditAuthorForm(FlaskForm):
    """
    Форма для редактирования автора в справочнике
    """
    name = StringField(label='Новое ФИО:',
                       validators=[
                           DataRequired('Данное поле обязательно'),
                           Regexp(regex=r'\A[А-Яа-я ]*\Z',
                                  message='Формат: Фамилия Имя Отчество, >2 символов в каждой части ФИО')
                       ],
                       render_kw={'placeholder': 'Введите ФИО автора'})
    submit = SubmitField('Изменить')


class AddFilmForm(FlaskForm):
    """
    Форма для добавления нового фильма
    """
    name = StringField(label='Название фильма:',
                       validators=[
                           DataRequired('Данное поле обязательно'),
                           Regexp(regex=r'\A[А-Яа-я0-9 ]{5,20}\Z',
                                  message='Диапазон значений: {А-Я, а-я, 1-9}. Длина названия должна составлять от 5 до 20 символов.')
                       ],
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
                       validators=[
                           DataRequired('Данное поле обязательно'),
                           Regexp(regex=r'\A[А-Яа-я0-9 ]{5,20}\Z',
                                  message='Диапазон значений: {А-Я, а-я, 1-9}. Длина названия должна составлять от 5 до 20 символов.')
                       ],
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
                           validators=[
                               DataRequired(
                                   'Данное поле обязательно'),
                               Regexp(regex=r'\A[0-9]{10}\Z',
                                      message='10 цифр')
                           ],
                           render_kw={'placeholder': 'Введите данные'})
    name = StringField(label='ФИО:',
                       validators=[
                           DataRequired('Данное поле обязательно'),
                           Regexp(regex=r'\A[А-Яа-я ]*\Z',
                                  message='Формат: Фамилия Имя Отчество, >2 символов в каждой части ФИО')
                       ],
                       render_kw={'placeholder': 'Введите ФИО'})
    post = SelectField(u'Должность', coerce=int)
    login = StringField(label='Логин:',
                        validators=[
                            DataRequired('Данное поле обязательно'),
                            Regexp(regex=r'\A[A-Za-z0-9]{5,20}\Z',
                                   message='Формат: Диапазон значений:[A-Za-z0-9], от 5 до 20 символов')
                        ],
                        render_kw={'placeholder': 'Введите логин'})
    password = StringField(label='Пароль:',
                           validators=[
                               DataRequired('Данное поле обязательно'),
                               Regexp(regex=r'\A[A-Za-z0-9]{5,20}\Z',
                                      message='Формат: Диапазон значений:[A-Za-z0-9], от 5 до 20 символов')
                           ],
                           render_kw={'placeholder': 'Введите пароль'})
    submit = SubmitField('Записать')


class CinemahallForm(FlaskForm):
    """ 
    Форма для добавления/изменения кинозала
    """
    name = StringField(label='Наименование:',
                       validators=[
                           DataRequired('Данное поле обязательно'),
                           Regexp(regex=r'\A[А-Я][а-я1-9 ]{4,19}\Z',
                                  message='Формат: с большой буквы, >5 символов')
                       ],
                       render_kw={'placeholder': 'Введите наименование'})
    capacity = IntegerField(label='Вместимость:',
                            validators=[
                                DataRequired('Данное поле обязательно'),
                                NumberRange(min=50, max=1000,
                                            message='от 50 до 1000')
                            ],
                            render_kw={'placeholder': 'Введите вместимость'})
    submit = SubmitField('Записать')


class FilmSessionForm(FlaskForm):
    """ 
    Форма для добавления/изменения сеанса
    """
    date_time = DateTimeLocalField(label='Дата и время:',
                                   format='%Y-%m-%dT%H:%M',
                                   validators=[DataRequired(
                                       'Данное поле обязательно')],
                                   render_kw={'placeholder': 'Введите дату и время'})
    name_film = SelectField(u'Название фильма')
    name_cinemahall = SelectField(u'Название кинозала')

    submit = SubmitField('Записать')
