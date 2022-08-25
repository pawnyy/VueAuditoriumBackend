from flask import request, url_for

from app import db
from app.items import bp
import app.filters as filters
from app.models import Item
from app.schemas import ItemSchema, AllItemSchema


@bp.route('/items', methods=['GET'])
def get_items():
    #  Get all items from the database
    items = Item.query.all()
    return AllItemSchema().jsonify(items, many=True)

@bp.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    #  Get item from the database
    item = Item.query.get(id)
    return ItemSchema().jsonify(item)


@bp.route('/items', methods=['POST'])
@filters.is_admin
def create_item():
    #  Create a new item in the database
    item = ItemSchema().load(request.get_json())
    item.id = None
    db.session.add(item)
    db.session.commit()
    return ItemSchema().jsonify(item), 201, {'Location': url_for('items.get_item', id=item.id, _external=True)}
