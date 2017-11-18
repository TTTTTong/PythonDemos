from FlaskDemo.exts import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'flask_user'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(11), nullable=False)
    user = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)