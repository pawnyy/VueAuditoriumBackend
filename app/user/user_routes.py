#
# Blueprint: User
#
# >> Make sure to import bp as the correct blueprint <<
#
from app.user import bp

from flask import jsonify, abort, request, g, current_app
from marshmallow import ValidationError
from app import filters, db, auth
from app.models import User, Checkout
from app.schemas import UserSchema, CheckoutSchema
from app.user import user_service as user_service


@bp.route('/checkToken', methods = ['GET'])
def check_token():
    return jsonify({"token": "valid"})


@bp.route('/users/me', methods = ['GET'])
def get_self():
    user = UserSchema().dump(g.user)
    return jsonify(user)


@bp.route('/users/<int:user_id>', methods = ['GET'])
@filters.is_admin
def get_user(user_id):
    user = UserSchema().dump(User.query.get_or_404(user_id))
    return jsonify(user)

@bp.route('/users/<int:user_id>/checkouts', methods = ['GET'])
@filters.is_admin
def get_checkouts(user_id):
    checkouts = Checkout.query.filter_by(user_id = user_id).all()
    return CheckoutSchema(many = True).jsonify(checkouts)


@bp.route('/users/<int:user_id>/change_password', methods = ['PATCH'])
@auth.login_required
def change_password(user_id):
    if user_id != g.user.id or not g.user.is_admin:
        abort(403)
    data = request.get_json() or {}
    user = User.query.get_or_404(user_id)
    if 'password' not in data:
        raise ValidationError('Password is required')
    user.set_password(data['password'])
    db.session.commit()
    return '', 200

@bp.route('/users/<int:user_id>', methods = ['PATCH'])
@filters.is_super_admin
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    if 'admin' in data:
        user.admin = data['admin']
    if 'superadmin' in data:
        user.superadmin = data['superadmin']
    db.session.commit()
    return UserSchema().jsonify(user)

@bp.route('/users', methods = ['POST'])
@filters.is_super_admin
def create_user():
    data = request.get_json() or {}
    try:
        user = UserSchema().load(data)
    except ValidationError as err:
        current_app.logger.error(err.messages)
        return jsonify(err.messages), 422
    db.session.add(user)
    db.session.commit()
    return jsonify(UserSchema().dump(user)), 201

#
# Get all users
#
@bp.route('/users', methods=['GET'])
@filters.is_admin
def get_users():
    users = User.query.all()
    data = UserSchema(many=True).dump(users)
    for user in data:
        user['total_checkouts'] = user_service.get_total_checkouts(user['id'])
    return jsonify(data)


