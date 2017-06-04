from flask import g, request, jsonify, abort
from flask_login import login_required
from app import app, db
from app.models import Bucketlist, Item


@app.route('/bucketlists/<int:id>/items/', methods=['POST'])
@login_required
def add_items_in_single_bucketlist(id):
    """Create a new item in bucket list"""
    if not request.json:
        abort(400)
    bucket = Bucketlist.query.filter_by(bucket_id=id).first()
    if not bucket or bucket.created_by != g.user_id:
        return jsonify(message='This bucketlist with id {} was not found!'.format(id)), 404

    item = Item(title=request.json('title'))
    item.bucketlist_id = bucket.id
    db.session.add(item)
    db.session.commit()
    return bucket, 201


@app.route('/bucketlists/<int:id>/items/<int:item_id>/', methods = ['PUT'])
@login_required
def update_single_item(id, item_id):
    """Update a bucket list item"""
    if not request.json:
        abort(400)

    bucket = Bucketlist.query.filter_by(bucket_id=id).first()
    if not bucket or bucket.created_by != g.user_id:
        return jsonify(message='This bucketlist with id {} was not found!'.format(id)), 404

    item = Item.query.get(item_id)
    if not item or (item.bucketlist_id != bucket.id):
        return jsonify(message='Item ID {0} doesn\'t exist!'.format(item_id))

    else:
        item.title = request.json.get('title')
        item.done = request.json.get('done')
        db.session.commit()
        return bucket, 200


@app.route('/bucketlists/<int:id>/items/<int:item_id>/', methods = ['DELETE'])
@login_required
def delete_an_item_from_a_single_bucketlist(id, item_id):
    """Delete an item in a bucket list"""
    if not request.json:
        abort(400)
    bucket = Bucketlist.query.filter_by(bucket_id=id).first()
    if not bucket or bucket.created_by != g.user_id:
        return jsonify(message='This bucketlist with id {} was not found!'.format(id)), 404
    item = Item.query.get(item_id)
    if not item or (item.bucketlist_id != bucket.id):
        return jsonify(message='Item ID {0} doesn\'t exist!'.format(item_id))
    else:
        db.session.delete(Item.query.get(item_id))
        db.session.commit()
        return jsonify({'Delete': True}), 200
