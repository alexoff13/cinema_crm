# https://www.askpython.com/python-modules/flask/flask-postgresql

from app import db
# relationship
# https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html


class Film(db.Model):
    """ 
    TODO docstring
    """
    __tablename__ = 'film'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    id_genre = db.Column(db.Integer, db.ForeignKey('genre.id'))

    def __init__(self, id, name, id_genre):
        self.id = id
        self.name = name
        self.id_genre = id_genre

    def __repr__(self):
        return f"{self.id} : {self.name} : {self.id_genre}"


class Genre(db.Model):
    """ 
    TODO docstring
    """
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    films = db.relationship("Film", back_populates="genre")

    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return f"{self.id}:{self.name}"

    

