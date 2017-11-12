from FlaskDemo.exts import db


class User(db.Model):
    __tablename__ = 'flask_user'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(11), nullable=False)
    user = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
