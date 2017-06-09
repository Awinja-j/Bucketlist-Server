import os
import inspect
import sys
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from flask import url_for, g, request, jsonify, abort
from run import db
from app.auth.auth import auths
from app.models import Bucketlist, Item
from flask.blueprints import Blueprint

bucket = Blueprint('bucket', __name__, template_folder='templates')


@bucket.route('/bucketlists/', methods=['GET'])
@auths.login_required
def get_all_bucketlists():
    """gets all the bucket lists"""
    page_no = request.args.get('page_no', 1)
    limit = request.args.get('limit', 20)
    q_name = request.args.get('q', "")
    bucket = Bucketlist.query.filter_by(created_by=g.user.id).\
        filter(Bucketlist.title.ilike('%{}%'.format(q_name))).paginate(
        int(page_no), int(limit)
    )
    if not bucket:
        return jsonify(message='There is No Bucketlist to display!!!!')
    else:
        bucketlists = [
            {
                "id":bucketlist.id,
                "title": bucketlist.title,
                "date_created": bucketlist.date_created,
                "date_modified": bucketlist.date_modified,
                "created_by": bucketlist.created_by
            }
            for bucketlist in bucket.items
        ]
        print(vars(bucket))
        return jsonify({
            "Bucketlists": bucketlists,
            "next": url_for(request.endpoint, page_no=bucket.next_num, limit=limit,
                            _external=True) if bucket.has_next else None,
            "prev": url_for(request.endpoint, page_no=bucket.prev_num, limit=limit,
                            _external=True) if bucket.has_prev else None,
        }), 200

@bucket.route('/bucketlists/', methods = ['POST'])
@auths.login_required
def new_bucketlist():
    """Create a new bucket list"""
    if not request.json:
        abort(400)
    bucketlist = Bucketlist(title=request.json['title'], created_by=g.user.id)
    db.session.add(bucketlist)
    db.session.commit()
    return jsonify(
                    {"id":bucketlist.id,
                    "title": bucketlist.title,
                    "date_created": bucketlist.date_created,
                    "date_modified": bucketlist.date_modified,
                    "created_by": bucketlist.created_by
                    }), 201


@bucket.route('/bucketlists/<int:id>', methods=['GET'])
@auths.login_required
def get_bucketlist(id):
    """Get single bucket list"""
    bucket = Bucketlist.query.filter_by(id=id).first()
    if not bucket or bucket.created_by != g.user.id:
        return jsonify(message='This bucketlist with id {} was not found!'.format(id)), 404

    bucket_items = Item.query.filter_by(bucketlist_id=bucket.id).all()
    if bucket_items is None:
        list_items = []
        print('This bucketlist does not contain any items.')
    else:
        list_items = [{
            "id": bucket_items.id,
            "title": bucket_items.title,
            "date_created": bucket_items.date_created,
            "date_modified": bucket_items.date_modified,
            "done": bucket_items.done
        } for bucket_item in bucket_items]
    return jsonify({
        "id": bucket.id,
        "title": bucket.title,
        "items": list_items,
        "date_created": bucket.date_created,
        "date_modified": bucket.date_modified,
        "created_by": bucket.created_by
    }), 200


@bucket.route('/bucketlists/<int:id>', methods = ['PUT'])
@auths.login_required
def put_bucketlist(id):
    """Update this bucket list"""
    if not request.json:
        abort(400)
    bucket = Bucketlist.query.filter_by(id=id).first()
    if not bucket or bucket.created_by != g.user.id:
        return jsonify(message='This bucketlist with id {} was not found!'.format(id)), 404
    else:
        bucket.title = request.json.get('title')
        db.session.commit()
        return jsonify({
            "id": bucket.id,
            "title": bucket.title,
            "date_created": bucket.date_created,
            "date_modified": bucket.date_modified,
            "created_by": bucket.created_by
        }), 201

@bucket.route('/bucketlists/<int:id>', methods = ['DELETE'])
@auths.login_required
def delete_bucketlist(id):
    """Delete this single bucket list"""

    bucket = Bucketlist.query.filter_by(id=id).first()
    if not bucket or bucket.created_by != g.user.id:
        return jsonify(message='This bucketlist with id {} was not found!'.format(id)), 404
    else:

        db.session.delete(Bucketlist.query.get(id))
        db.session.commit()
        return jsonify({'Delete': True}), 200

def bucket_search():
    """search for a single bucketlist using name"""
    bucketlist = Bucketlist.query.filter(Bucketlist.title.ilike('%' + search + '%')).filter_by(user_id=user.id)