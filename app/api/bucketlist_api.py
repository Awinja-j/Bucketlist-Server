from flask import g, request, jsonify, abort
from app import app, db
from app.auth.auth import auth
from flask_login import login_required
from app.models import Bucketlist

@app.route('/bucketlists/', methods = ['GET'])
@login_required
def get_all_bucketlists(self):
    """gets all the bucket lists"""
    bucket = Bucketlist.query.filter_by(created_by=g.user_id)
    if not bucket or bucket.created_by != g.user_id:
        return jsonify(message='There is No Bucketlist to display!!!!')
    else:
        return bucket, 200

@app.route('/bucketlists/', methods = ['POST'])
@login_required
def new_bucketlist():
    """Create a new bucket list"""
    if not request.json:
        abort(400)
    bucketlist = Bucketlist(title=request.get.json('title'), created_by=g.user_id)
    db.session.add(bucketlist)
    db.session.commit()
    return bucketlist, 201

@app.route('/bucketlists/<int:id>', methods = ['GET'])
@login_required
def get_bucketlist(id):
    """Get single bucket list"""
    if not request.json:
        abort(400)
    bucket = Bucketlist.query.filter_by(bucket_id=id).first()
    if not bucket or bucket.created_by != g.user_id:
        return jsonify(message='This bucketlist with id {} was not found!'.format(id)), 404
    else:
        return bucket, 200

@app.route('/bucketlists/<int:id>', methods = ['PUT'])
@login_required
def put_bucketlist(self, id):
    """Update this bucket list"""
    if not request.json:
        abort(400)
    bucket = Bucketlist.query.filter_by(bucket_id=id).first()
    if not bucket or bucket.created_by != g.user_id:
        return jsonify(message='This bucketlist with id {} was not found!'.format(id)), 404
    else:
        bucket.title = request.json.get('title')
        db.session.commit()
        return bucket, 200


@app.route('/bucketlists/<int:id>', methods = ['DELETE'])
@login_required
def delete_bucketlist(id):
    """Delete this single bucket list"""
    if not request.json:
        abort(400)
    bucket = Bucketlist.query.filter_by(bucket_id=id).first()
    if not bucket or bucket.created_by != g.user_id:
        return jsonify(message='This bucketlist with id {} was not found!'.format(id)), 404
    else:
        db.session.delete(Bucketlist.query.get(id))
        db.session.commit()
        return jsonify({'Delete': True}), 200
