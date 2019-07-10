from app import db

from werkzeug.security import generate_password_hash, check_password_hash
import enum


#
# Enum: User Type
#
class UserType(enum.Enum):
    admin = "admin"
    user = "user"


#
# Model: Base
#
class BaseModel(db.Model):
    __abstract__ = True

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


#
# Model: User
#
class User(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    type = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute.')

    # @password.setter
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def is_admin(self):
        return self.type == UserType.admin.value
