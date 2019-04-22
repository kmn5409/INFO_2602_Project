from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, render_template, make_response
from sqlalchemy import func
from sqlalchemy.event import listen
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

# Setting up Logging Functionality (using file-based logging)
logHandler = RotatingFileHandler('info.log', maxBytes=1000, backupCount=1)
logHandler.setLevel(logging.INFO)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(logHandler)
log = app.logger

# enable CORS on all the routes that start with /api
CORS(app, resources={r"/*": {"origins": "*"}})
g = Github()

# configure the database to use Flask Sessions
db = SQLAlchemy(app)
session = db.session

from models.pull_request import PullRequest
from models.pull_request import Comment
from models.pull_request import ReviewComment
from models.users import User
    
def authenticate():
    """
    The Authenticate function is used primarily by the JWT library to determine if submitted credentials match
    :param username: Unique username for the user
    :param password: Password used to verify user account
    :return: returns an instance of the user model
    """
    try:
        # Fetch user using the username (case insensitive search)
        name = g.get_user().login
        #print(name)
        return True
    except Exception as e:
        log.error("Authenticate: {0}".format(e))
    # We failed authentication either due to incorrect credentials or server error
    return False

def load_file_into_table(new_user):
    import json
    db.Model.metadata.drop_all(bind=db.engine)
    db.Model.metadata.create_all(bind=db.engine)
    p = ""
    rID=0
    user=new_user['user_name']
    name=new_user["repo_name"]
    try:
        for repo in g.get_user(user).get_repos():
            if(repo.name == name):
                print(repo.name)
                for pull_request in repo.get_pulls():
                    print(1)
                    p = PullRequest()
                    p.fromJSON(pull_request,repo.name)
                    print(2)
                    print("Pull Request:")
                    db.session.add(p)
                    rID+=1
                    print(p.toDict())
                    for comment in pull_request.get_issue_comments():
                        #print("Comments: \n\n",comment.body)
                        c = Comment()
                        #print(comment)
                        c.fromJSON(comment,rID)
                        #print("Before")
                        db.session.add(c)
                        print("Comment")
                        print(c.toDict())
                db.session.commit()
                return {"message":'Repo created', "code":201}
        return {"message":'Repo not found', "code":404}
    except:
        return {"Exception message":'Repo not found', "code":404}


@app.before_first_request
def setup():
    db.Model.metadata.drop_all(bind=db.engine)
    db.Model.metadata.create_all(bind=db.engine)

@app.route('/')
def hello():
    return '<h1>Hello World</h1>'

def createLogin(new_person):
    try:
        global g
        g = Github(new_person['name'],new_person['password'])
        print("Logged in")
    except error:
        return {"message":"Error "+error, "code":500}
    finally:
        return {"message":'Logged in', "code":201}

#check log in status
@app.route('/api')
def github():
    try:
        name = g.get_user().login
    except:
        return render_template("login.html")
    return user_form()

@app.route('/api/login', methods=['POST'])
def api_create_person():
    data = None
    if request.content_type  == 'application/x-www-form-urlencoded':
        data = request.form
    elif request.content_type == 'application/json':
        data = request.json
    result=createLogin(data)# call createPerson on data an jsonify its response
    print(result)
    if result['code']==201:
        return user_form()
    return render_template("login.html")


@app.route("/api/load_repos", methods=["POST"])
def find_repos():
    data = None
    if request.content_type  == 'application/x-www-form-urlencoded':
        data = request.form
    elif request.content_type == 'application/json':
        data = request.json
    result=load_file_into_table(data)
    if result['code']==201:
        print(result)
        return show_all_pull_requests()
    print(result)
    return render_template("get_user.html", message="Seems like that isn't a valid repository.")

@app.route('/protected')
@app.route('/api/get_repos')
def user_form():
    if(authenticate() == False):
        print("Here")
        return render_template("login.html")
    return render_template("get_user.html", message="")

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
    response = records
    return render_template('request.html', requests=records)

@app.route('/api/all_pull_requests', methods=['GET'])
def get_all_pull_requests():
    query = PullRequest.query.order_by(PullRequest.id.asc())
    start = request.args.get('offset', default=1, type=int)
    num_records = request.args.get('limit', default=10, type=int)
    records = query.paginate(start, num_records).items
    records = list(map(lambda x: x.toDict(), records))
    print(len(records))
    print(records)
    return jsonify(records)


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
        pull_request = PullRequest.query.get(fk_id)
        if comment:
            results=list(map(lambda x: x.toDict(), comment))
            return render_template('comments.html',comments=results, request=pull_request)
        else:
            results = None
            return render_template("error.html", error="We couldn't find that.  404")
    except Exception as e:
        print(e)
        return render_template("error.html", error="Server error.  500")

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
            pull= PullRequest.query.get(fk_id)
            print(pull)
            results=(list(map(lambda x: x.toDict(), review)))
            return render_template('review.html',reviews=results, request=pull)
        else:
            results = None
            return render_template("error.html", error="We couldn't find that.  404")
    except Exception as e:
        print(e)
        return render_template("error.html", error="Server error.  500")

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

def updateReviewComment(new_review,pk_id):
    try:
        review=ReviewComment.query.get(pk_id)
        review.comment_content=new_review["comment_content"]
        review.timestamp=func.now()
        db.session.commit()
        print(review.toDict())
        return {"message":" Success", "code":202}
    except Exception as e:
        return {'error': 'Server encountered an error. ' + e, "code": 500}


@app.route('/protected')
@app.route('/api/pull_requests/new_comment/<pk_id>', methods=['GET'])
def make_new_comment(pk_id):
    if(authenticate() == False):
        print("Here")
        return render_template("login.html")
    pull_request = PullRequest.query.get(pk_id)
    return render_template('form.html', pull_request=pull_request)

@app.route('/protected')
@app.route('/api/pull_requests/update_comment/<pk_id>', methods=['GET'])
def update_comment(pk_id):
    if(authenticate() == False):
        print("Authentication failed")
        return render_template("login.html")
    review = ReviewComment.query.get(pk_id)
    return render_template('form.html', review=review, pull_request=None)

@app.route('/api/pull_requests/process_comment/<fk_id>', methods=['POST', 'GET'])
def process_form(fk_id):
    if request.content_type  == 'application/x-www-form-urlencoded': 
        result=createReveiwComment(request.form)
        if result['code']==201:
            print(make_response(jsonify(result)))
            return get_pull_reviews_by_id(fk_id)
    return make_response(jsonify({'error': 'Server encountered an error'}),500)

@app.route('/api/pull_requests/process_update/<pk_id>', methods=['POST', 'GET'])
def update_form(pk_id):
    if request.content_type  == 'application/x-www-form-urlencoded': 
        result=updateReviewComment(request.form,pk_id)
        if result['code']==202:
            rvw=ReviewComment.query.get(pk_id)
            print(make_response(jsonify(result)))
            return get_pull_reviews_by_id(rvw.request_id)
    return make_response(jsonify({'error': 'Server encountered an error'}),500)

@app.route('/protected')
@app.route('/api/pull_requests/stats')
def return_stats():
    if(authenticate() == False):
        print("Authentication failed")
        return render_template("login.html")
    return render_template('stats.html') 

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

@app.route('/protected')
@app.route('/api/pull_requests/<pk_id>/comment/delete',methods=['GET','DELETE'])
def delete_comment(pk_id):
    if(authenticate() == False):
        print("Authentication failed")
        return render_template("login.html")
    comment = Comment.query.get(pk_id)
    pull_request = PullRequest.query.get(comment.request_id)
    user_name = g.get_user().login
    if(comment.commentor_name != user_name and pull_request.repos_author != user_name and pull_request.author_name!=user_name):
        render_template("error.html",error="Doesn't seem like you have enough priviliges to do this. 403")
    print(pull_request.repo_name)
    g.get_user(pull_request.repos_author).get_repo(pull_request.repo_name).get_pull(pull_request.number).get_issue_comment(comment.comment_id).delete()
    db.session.delete(comment)
    print("Deleted comment")
    db.session.commit()
    return get_pull_comments_by_id(pull_request.id)

@app.route('/protected')
@app.route ('/api/pull_requests/post_comment/<pk_id>', methods=['POST', 'GET'])
def post_comment(pk_id):
    if(authenticate() == False):
        print("Authentication failed")
        return render_template("login.html")
    review_comment = ReviewComment.query.get(pk_id)
    fk_id = review_comment.request_id
    pull_request = PullRequest.query.get(review_comment.request_id)
    g.get_user(pull_request.repos_author).get_repo(pull_request.repo_name).get_pull(pull_request.number).create_issue_comment(review_comment.comment_content)
    db.session.delete(review_comment)
    print("deleted reveiw.")
    db.session.commit()
    print(pk_id)
    return get_pull_reviews_by_id(fk_id)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_reloader=True)