from app import ma
from flask import current_app
from app.models import User, Item
from marshmallow import fields, validates, validates_schema, ValidationError

import re


class ItemSchema(ma.ModelSchema):
    class Meta:
        model = Item

    quantity = fields.Method('get_quantity')

    def get_quantity(self, obj):
        return obj.quantity()

class AllItemSchema(ma.ModelSchema):
    class Meta:
        model = Item
        exclude = ('checkouts', 'created', 'updated')

    quantity = fields.Method('get_quantity')

    def get_quantity(self, obj):
        return obj.quantity()


#
# Common representation of a User
#
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        exclude = ['password']


#
# Validates user registration input.
#
class UserRegistrationSchema(ma.ModelSchema):
    username = fields.String(required = True)
    email = fields.String(required = True)
    password = fields.String(required = True)

    @validates_schema
    def validate_registration(self, data, **kwargs):
        # Create error
        userinfo = data
        valerr = ValidationError({})
        foundError = False

        if "username" not in userinfo or userinfo["username"] == "":
            valerr.messages["username"] = "Username field is blank."
            foundError = True
        elif len(userinfo["username"]) < 3:
            valerr.messages["username"] = "Username is too short."
            foundError = True

        if "email" not in userinfo or userinfo["email"] == "":
            valerr.messages["email"] = "Email field is blank."
            foundError = True
        elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", userinfo["email"]):
            valerr.messages["email"] = "Invalid email address."
            foundError = True

        if "password" not in userinfo or userinfo["password"] == "":
            valerr.messages["password"] = "Password field is blank."
            foundError = True
        elif len(userinfo["password"]) < 4:
            valerr.messages["password"] = "Password is too short. Must be 4 or more characters"
            foundError = True

        if foundError:
            raise valerr

    class Meta:
        model = User


#
# Common representation of a Post
#
# class
