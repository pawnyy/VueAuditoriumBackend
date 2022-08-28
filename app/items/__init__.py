from flask import Blueprint

from app import auth

bp = Blueprint('items', __name__)


@bp.before_request
@auth.login_required
def restrict_bp_to_admins():
    pass


from app.items import items_routes
