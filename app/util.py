from app import db
from datetime import datetime
from flask_login import current_user


def check_session_time(name_cinemahall: str, date_time: datetime) -> list:
    """
    Функция для проверки добавления сеанса, возвращает список конфликтующих сеансов по времени
    """
    check_sessions = db.engine.execute(
        f"""
        select
            s.name_film               as film_name
            ,s.date_time              as start
            ,s.date_time + f.duration as end
        from
            session_film as s
                inner join film f on f.name = s.name_film 
        where 
            s.name_cinemahall = '{name_cinemahall}'
            and '{str(date_time)}' between s.date_time and s.date_time + f.duration
        
        """
    ).fetchall()
    return check_sessions


def get_post_for_user() -> int:
    """Функция для возвращения должности пользователя 

    :return: id должности, либо 0, если пользователь не авторизован
    """
    try:
        post_id = current_user.post_id
        print(post_id)
        return post_id
    except AttributeError:
        return 0
