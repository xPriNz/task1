from project import db, app
import bleach

# Book model
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    author = db.Column(db.String(64))
    year_published = db.Column(db.Integer)
    book_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default='available')

    def __init__(self, name, author, year_published, book_type, status='available'):

        # Sanitize input using Bleach
        self.name = bleach.clean(name, strip=True)
        self.author = bleach.clean(author, strip=True)
        self.year_published = year_published
        self.book_type = bleach.clean(book_type, strip=True)
        self.status = bleach.clean(status, strip=True)

    def __repr__(self):
        return (f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, "
                f"Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})")

with app.app_context():
    db.create_all()