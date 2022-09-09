from flask import request, url_for, g

from app import db
from app.items import bp
import app.filters as filters
from app.models import Item, Checkout
from app.schemas import ItemSchema, AllItemSchema, CheckoutSchema


@bp.route('/items/<int:id>/checkouts', methods = ['GET'])
@filters.is_admin
def get_checkouts(id):
    item = Item.query.get_or_404(id)
    checkouts = item.checkouts.all()
    return CheckoutSchema(many = True).jsonify(checkouts)


@bp.route('/checkouts/<int:id>', methods = ['PATCH'])
@filters.is_admin
def update_checkout(id):
    checkout = Checkout.query.get_or_404(id)
    data = request.get_json() or {}
    if 'returned' in data:
        checkout.returned = data['returned']
    db.session.commit()
    return CheckoutSchema().jsonify(checkout)


@bp.route('/items/checkout', methods = ['POST'])
def checkout_item():
    data = request.get_json()
    item = Item.query.get_or_404(data['item_id'])
    if item.quantity() < data['quantity']:
        return '', 400

    del data['item_id']

    checkout = CheckoutSchema().load(data)
    checkout.user_id = g.user.id
    checkout.item_id = item.id
    db.session.add(checkout)
    db.session.commit()
    return '', 200


@bp.route('/items', methods = ['GET'])
def get_items():
    #  Get all items from the database
    items = Item.query.all()
    return AllItemSchema().jsonify(items, many = True)


@bp.route('/items/<int:id>', methods = ['DELETE'])
@filters.is_admin
def delete_item(id):
    #  Delete an item from the database
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return '', 204


@bp.route('/items/<int:id>', methods = ['GET'])
def get_item(id):
    #  Get item from the database
    item = Item.query.get(id)
    return ItemSchema().jsonify(item)


@bp.route('/items', methods = ['POST'])
@filters.is_admin
def create_item():
    #  Create a new item in the database
    item = ItemSchema().load(request.get_json())
    item.id = None
    db.session.add(item)
    db.session.commit()
    return ItemSchema().jsonify(item), 201, {'Location': url_for('items.get_item', id = item.id, _external = True)}


@bp.route('/items/<int:id>', methods = ['PUT'])
@filters.is_admin
def update_item(id):
    #  Update an item in the database
    item = Item.query.get(id)
    if item is None:
        return '', 404
    item = ItemSchema().load(request.get_json(), instance = item)
    db.session.commit()
    return ItemSchema().jsonify(item)
