#
# Blueprint: User
#
# >> Make sure to import bp as the correct blueprint <<
#
from app.user import bp

from flask import jsonify, abort, request, g, current_app
from marshmallow import ValidationError
from app import filters, db
from app.models import User
from app.schemas import UserSchema
from app.user import user_service as user_service


@bp.route('/checkToken', methods = ['GET'])
def check_token():
    return jsonify({"token": "valid"})


@bp.route('/users/me', methods = ['GET'])
def get_self():
    user = UserSchema().dump(g.user)
    return jsonify(user)


#
# Get all users
#
@bp.route('/users')
@filters.is_admin
def get_users():
    users = User.query.all()
    return UserSchema().jsonify(users, many = True)


