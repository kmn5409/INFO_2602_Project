from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from models.entity import Entity
from sqlalchemy.event import listen
import csv
from sqlalchemy.sql import func
from github import Github

from app import db

class PullRequest(Entity,db.Model):
    __tablename__ = 'pullRequest'
    #id = Column(Integer,primary_key=True,autoincrement='auto')
    repos_author = Column(String(50))
    repo_name = Column(String(100))
    #repo = Column(String(100))
    author_name = Column(String(50))
    pull_request_message = Column(String(5000))
    pull_request_comment = Column(String(5000))
    number = Column(Integer)
    #pull_request_id = Column(String(50))
    url = Column(String(50))
    timestamp = Column(DateTime())
    

    def __init__(self):
        super().__init__()
        Entity.__init__(self)

    def fromJSON(self,pull_request):
        self.repos_author = pull_request.base.repo.owner.login
        self.repo_name = repo_name
        #self.repo = repo
        self.author_name = pull_request.user.login #Need to verify if this is the author
        self.pull_request_message = pull_request.title
        self.pull_request_comment = pull_request.body
        self.number = pull_request.number
        self.timestamp = pull_request.created_at
        self.url = pull_request.html_url

    def toDict(self):
        repre = Entity.toDict(self)
        repre.update({
            'id':self.id,
            'repo_name':self.repo_name,
            'repository_owner':self.repos_author,
            'author_name':self.author_name,
            'pull_request_comment': self.pull_request_comment,
            'pull_request_message' : self.pull_request_message,
            'author_name':self.author_name,  
            'timestamp':  self.timestamp,
            'url':self.url
        })
        return repre


class Comment(db.Model):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    commentor_name = Column(String(50))
    comment_content = Column(String(5000))
    timestamp = Column(DateTime())    
    #request_id = Column(Integer, ForeignKey('pullRequest.id'))
    request_id = Column(Integer, ForeignKey('pullRequest.id'), nullable=False)

    def __init__(self):
        super().__init__()
        #Entity.__init__(self)

    def fromJSON(self,comment,id1):
        
        self.commentor_name = comment.user.login
        self.comment_content = comment.body
        self.timestamp = comment.created_at
        self.request_id = id1

    def toDict(self):
        #repre = Entity.toDict(self)
        return {
            'id':self.id,
            'commentor_name':self.commentor_name,
            'comment_content':self.comment_content,
            'timestamp':self.timestamp,
            'request_id':self.request_id
        }
        
class ReviewComment(db.Model):
    __tablename__ = 'reveiws'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    comment_content = Column(String(5000))
    timestamp = Column(DateTime(), server_default=func.now())    
    request_id = Column(Integer, ForeignKey('pullRequest.id'), nullable=False)

    def __init__(self):
        super().__init__()

    def toDict(self):
        return {
            'id':self.id,
            'comment_content':self.comment_content,
            'timestamp':self.timestamp,
            'request_id':self.request_id
        }


