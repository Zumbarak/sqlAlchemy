from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    library = db.relationship(
        "Library", backref="user", uselist=False, cascade="all, delete-orphan"
    )


class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    library_id = db.Column(db.Integer, db.ForeignKey("library.id"))
    created_at = db.Column(db.DateTime)
