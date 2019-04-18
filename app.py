from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, render_template, make_response
from sqlalchemy import func
from flask_cors import CORS
import hashlib  
import logging
from werkzeug.security import safe_str_cmp
from logging.handlers import RotatingFileHandler
from github import Github

#How to do secure part of the lab
from flask_jwt import JWT, jwt_required, current_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Requests.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'so unsecured'
app.config['TEMPLATES_AUTO_RELOAD'] = True
# enable CORS on all the routes that start with /api
CORS(app, resources={r"/*": {"origins": "*"}})
g = Github("c5c1fb044b46cde5a102ae0f507309e01f68d593")

# configure the database to use Flask Sessions
db = SQLAlchemy(app)
session = db.session

from models.pull_request import PullRequest
from models.pull_request import Comment
from models.pull_request import ReviewComment
from models.users import User

@app.before_first_request
def setup():
    db.Model.metadata.drop_all(bind=db.engine)
    db.Model.metadata.create_all(bind=db.engine)


@app.route('/')
def hello():
    return '<h1>Hello World</h1>'

@app.route('/api/pull_requests', methods=['GET'])
def show_all_pull_requests():
    query = PullRequest.query.order_by(PullRequest.id.asc())
    
    start = request.args.get('offset', default=1, type=int)
    num_records = request.args.get('limit', default=10, type=int)

    records = query.paginate(start, num_records).items
    records = list(map(lambda x: x.toDict(), records))
    print(len(records))
    print(records)
    response = jsonify(records)
    #response = records
    return response

@app.route('/api/comments', methods=['GET'])
def show_all_comments():
    query = Comment.query.order_by(Comment.id.asc())
    
    start = request.args.get('offset', default=1, type=int)
    num_records = request.args.get('limit', default=10, type=int)

    records = query.paginate(start, num_records).items
    records = list(map(lambda x: x.toDict(), records))
    print(len(records))
    print(records)
    response = jsonify(records)
    return response


@app.route('/api/pull_requests/<pk_id>',methods=["GET"])
def get_pull_requests_by_id(pk_id):
    try:
        pull_request = PullRequest.query.get(pk_id)
        if pull_request:
            return jsonify(pull_request.toDict())
        else:
            results = None
            return make_response(jsonify(results), 404)
    except Exception as e:
        print(e)
        return make_response(jsonify({'error': 'Server encountered an error. Contact administrator'}), 500)

@app.route('/api/comments/<pk_id>',methods=["GET"])
def get_comments_by_id(pk_id):
    try:
        comment = Comment.query.get(pk_id)
        if comment:
            return jsonify(comment.toDict())
        else:
            results = None
            return make_response(jsonify(results), 404)
    except Exception as e:
        print(e)
        return make_response(jsonify({'error': 'Server encountered an error. Contact administrator'}), 500)

@app.route('/api/request_comments/<fk_id>',methods=["GET"])
def get_pull_comments_by_id(fk_id):
    try:
        comment=Comment.query.filter(Comment.request_id==fk_id)
        if comment:
            return jsonify(list(map(lambda x: x.toDict(), comment)))
        else:
            results = None
            return make_response(jsonify(results), 404)
    except Exception as e:
        print(e)
        return make_response(jsonify({'error': 'Server encountered an error'}),500)

@app.route('/api/review_comments', methods=['GET'])
def show_all_review_comments():
    query = ReviewComment.query.order_by(ReviewComment.id.asc())
    start = request.args.get('offset', default=1, type=int)
    num_records = request.args.get('limit', default=10, type=int)
    records = query.paginate(start, num_records).items
    records = list(map(lambda x: x.toDict(), records))
    print(len(records))
    print(records)
    response = jsonify(records)
    return response

@app.route('/api/request_review_comments/<fk_id>',methods=["GET"])
def get_pull_reviews_by_id(fk_id):
    try:
        review=ReviewComment.query.filter(ReviewComment.request_id==fk_id)
        if review:
            return jsonify(list(map(lambda x: x.toDict(), review)))
        else:
            results = None
            return make_response(jsonify(results), 404)
    except Exception as e:
        print(e)
        return make_response(jsonify({'error': 'Server encountered an error'}),500)

def createReveiwComment(new_reveiw_comment):
    try:
        comment=ReviewComment()
        comment.comment_content=new_reveiw_comment["comment_content"]
        comment.request_id=new_reveiw_comment["request_id"]
        db.session.add(comment)
        db.session.commit()
        return {"message":" Success", "code":201}
    except Exception as e:
        print(e)
        return {'error': 'Server encountered an error', "code": 500}


@app.route('/api/pull_requests/new_comment/<pk_id>', methods=['GET'])
def make_new_comment(pk_id):
    pull_request = PullRequest.query.get(pk_id)
    return render_template('form.html', pull_request=pull_request)

@app.route('/api/pull_requests/process_comment/<fk_id>', methods=['POST', 'GET'])
def process_form(fk_id):
    if request.content_type  == 'application/x-www-form-urlencoded': 
        result=createReveiwComment(request.form)
        if result['code']==201:
            print(make_response(jsonify(result)))
            return get_pull_reviews_by_id(fk_id)
    return make_response(jsonify({'error': 'Server encountered an error'}),500)

@app.route('/api/pull_requests/<fk_id>/review_comment/<pk_id>/delete', methods=['DELETE', 'GET'])
def delete_review_comment(fk_id, pk_id):
    try:
        reveiw=ReviewComment.query.get(pk_id)
        print("Got reveiw.")
        db.session.delete(reveiw)
        print("deleted reveiw.")
        db.session.commit()
    except Exception as  e:
        print({"message":"Database error", "code":500})
    return get_pull_reviews_by_id(fk_id)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_reloader=True)