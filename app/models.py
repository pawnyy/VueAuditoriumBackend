# from sqlalchemy import ARRAY
from sqlalchemy.orm import relationship

from app import db

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import Timestamp
from sqlalchemy_continuum import make_versioned
from sqlalchemy_continuum.plugins import ActivityPlugin
import sqlalchemy as sa

import enum

# Setup Activity Plugin
activity_plugin = ActivityPlugin()
make_versioned()


#
# Enum: User T


#
class BaseModel(db.Model, Timestamp):
    __abstract__ = True


class User(BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default = False)
    superadmin = db.Column(db.Boolean, default = False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def is_admin(self):
        return self.admin

    def is_superadmin(self):
        return self.superadmin



class Item(BaseModel):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True)
    description = db.Column(db.String(2048), index = True)
    max_quantity = db.Column(db.Integer, index = True)
    checkouts = db.relationship('Checkout', backref = 'item', lazy = 'dynamic')

    @property
    def quantity(self):
        quantity = 0
        for checkout in self.checkouts:
            quantity += checkout.quantity
        return quantity


class Checkout(BaseModel):
    __tablename__ = 'checkouts'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    quantity = db.Column(db.Integer, index = True)
    return_date = db.Column(db.DateTime, index = True)


sa.orm.configure_mappers()
Activity = activity_plugin.activity_cls
