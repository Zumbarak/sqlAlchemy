from app import db

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    library_id = db.Column(db.Integer, db.ForeignKey('library.id'))
    created_at = db.Column(db.DateTime)

    def __init__(self, title, author, library_id, created_at):
        self.title=title
        self.author=author
        self.library_id=library_id
        self.created_at=created_at