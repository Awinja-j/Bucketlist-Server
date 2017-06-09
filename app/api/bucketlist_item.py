import os
import inspect
import sys
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from flask import g, request, jsonify, abort
from app.auth.auth import auths
from run import db
from app.models import Bucketlist, Item
from flask.blueprints import Blueprint
POSTS_PER_PAGE = 20

item = Blueprint('item', __name__, template_folder='templates')



@item.route('/bucketlists/<int:id>/items', methods=['POST'])
@auths.login_required
def add_items_in_single_bucketlist(id):
    """Create a new item in bucket list"""
    if not request.json:
        abort(400)
    bucket = Bucketlist.query.filter_by(id=id).first()
    if not bucket or bucket.created_by != g.user.id:
        return jsonify(message='This bucketlist with id {} was not found!'.format(id)), 404

    item = Item(title=request.json['title'], bucketlist_id=bucket.id)
    db.session.add(item)
    db.session.commit()
    return jsonify({"id": item.id,
                    "title": item.title,
                    "date_created": item.date_created,
                    "date_modified": item.date_modified,
                    "done" : item.done,
                    "bucketlist_id": item.bucketlist_id
                    }), 201


@item.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT'])
@auths.login_required
def update_single_item(id, item_id):
    """Update a bucket list item"""
    if not request.json:
        abort(400)

    bucket = Bucketlist.query.filter_by(id=id).first()
    if not bucket or bucket.created_by != g.user.id:
        return jsonify(message='This bucketlist with id {} was not found!'.format(id)), 404

    item = Item.query.get(item_id)
    if not item or (item.bucketlist_id != bucket.id):
        return jsonify(message='Item ID {0} doesn\'t exist!'.format(item_id))

    else:
        item.title = request.json.get('title')
        item.done = request.json.get('done')
        db.session.commit()
        return jsonify(message='{} updated succesfully!'.format(item_id)), 200


@item.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['DELETE'])
@auths.login_required
def delete_an_item_from_a_single_bucketlist(id, item_id):
    """Delete an item in a bucket list"""

    bucket = Bucketlist.query.filter_by(id=id).first()
    if not bucket or bucket.created_by != g.user.id:
        return jsonify(message='This bucketlist with id {} was not found!'.format(id)), 404

    item = Item.query.get(item_id)
    if not item or (item.bucketlist_id != bucket.id):
        return jsonify(message='Item ID {0} doesn\'t exist!'.format(item_id))
    else:
        db.session.delete(Item.query.get(item_id))
        db.session.commit()
        return jsonify({'Delete': True}), 200

def item_search():
    """search for a single item using name"""