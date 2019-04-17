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
# enable CORS on all the routes that start with /api
CORS(app, resources={r"/*": {"origins": "*"}})
g = Github("c5c1fb044b46cde5a102ae0f507309e01f68d593")

# configure the database to use Flask Sessions
db = SQLAlchemy(app)
session = db.session

from models.pull_request import PullRequest
from models.pull_request import Comment
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
    #response = records
    return response


@app.route('/api/pull_requests/<pk_id>',methods=["GET"])
def get_pull_requests_by_id(pk_id):
    try:
        pull_request = PullRequest.query.get(pk_id)
        '''
        if request.form
            request_data = request.form
        else:
            request_data = request.get_json()
        '''
        if pull_request:
            return jsonify(pull_request.toDict())
        else:
            results = None
            return make_response(jsonify(results), 404)
    except Exception as e:
        print(e)
        return make_response(jsonify({'error': 'Server encountered an error. Contact administrator'}), 500)


'''
@app.route('/api/anime/<message>',methods=["POST"])
def get_pokemon_by_id(message):
    try:
        anime = Anime.query.get(pk_id)
        if anime:
            return jsonify(anime.toDict())
        else:
            results = None
            return make_response(jsonify(results), 404)
    except Exception as e:
        print(e)
        return make_response(jsonify({'error': 'Server encountered an error. Contact administrator'}), 500)

'''

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
