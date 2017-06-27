import os
import inspect
import sys
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from flask import url_for, g, request, jsonify, abort
from app.auth.auth import auths
from run import db
from app.models import Bucketlist, Item
from flask.blueprints import Blueprint

item = Blueprint('item', __name__, template_folder='templates')

@item.route('/bucketlists/<int:id>/items', methods=['GET'])
@auths.login_required
def get_all_items(id):
    """gets all the items in the bucket lists"""
    bucket = Bucketlist.query.filter_by(id=id).first()
    if not bucket or bucket.created_by != g.user.id:
        return jsonify(message='This bucketlist with id {} was not found!'.format(id)), 404

    page_no = request.args.get('page_no', 1)
    limit = request.args.get('limit', 20)
    q_name = request.args.get('q', "")

    item = Item.query.filter_by(bucketlist_id=bucket.id).\
        filter(Item.title.ilike('%{}%'.format(q_name))).paginate(
        int(page_no), int(limit)
    )

    if not item:
        return jsonify(message='There is No item to display!!!!')
    else:
        Items = [
            {
                "id": ITEM.id,
                "title": ITEM.title,
                "date_created": ITEM.date_created,
                "date_modified": ITEM.date_modified,
                "done":ITEM.done
            }
            for ITEM in item.items
        ]
        return jsonify({
            "Items": Items,
            "next": url_for(request.endpoint, page_no=item.next_num, limit=limit,
                            _external=True) if item.has_next else None,
            "prev": url_for(request.endpoint, page_no=item.prev_num, limit=limit,
                            _external=True) if item.has_prev else None,
        }), 200



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
    if not Item:
        return jsonify(message='This Item title already Exists'), 404
    else:
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
