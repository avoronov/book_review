from gino.ext.sanic import Gino

db = Gino()


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer(), primary_key=True)
    last_name = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String, nullable=False)
    brief = db.Column(db.String, nullable=False)
    rate = db.Column(db.Integer, nullable=False, default=0)
    author_id = db.Column(None, db.ForeignKey('authors.id'))
    publisher_id = db.Column(None, db.ForeignKey('publishers.id'))


class Publisher(db.Model):
    __tablename__ = 'publishers'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String, nullable=False)
