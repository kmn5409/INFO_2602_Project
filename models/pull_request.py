from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from models.entity import Entity
from sqlalchemy.event import listen
import csv
from github import Github


from app import db


#https://afternoon-refuge-76633.herokuapp.com/api/pokemon
#https://pacific-mesa-82818.herokuapp.com/ | https://git.heroku.com/pacific-mesa-82818.git
#https://devcenter.heroku.com/articles/git

class PullRequest(Entity,db.Model):
    __tablename__ = 'pullRequest'
    #id = Column(Integer,primary_key=True,autoincrement='auto')
    user = Column(String(50))
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
        #print("Here ",json_rec.commit.author.name)
        self.user = pull_request.user.login
        #self.repo = repo
        self.author_name = pull_request.user.login #Need to verify if this is the author
        self.pull_request_message = pull_request.title
        self.pull_request_comment = pull_request.body
        self.number = pull_request.number
        self.timestamp = pull_request.created_at
        self.url = pull_request.url

    def toDict(self):
        repre = Entity.toDict(self)
        repre.update({
            'id':self.id,
            'author_name':self.user,
            'pull_request_message' : self.pull_request_message,
            'pull_request_comment': self.pull_request_comment,
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
        
    

def load_file_into_table(target1, connection, **kw):
    import json
    g = Github("c5c1fb044b46cde5a102ae0f507309e01f68d593")
    user = "kmn5409"
    name = "Test"
    p = ""
    rID=0
    for repo in g.get_user(user).get_repos():
        if(repo.name == name):
            for pull_request in repo.get_pulls():
                #print("Message: ",i.commit.message[:])
                p = PullRequest()
                #print(i)
                #print(i.commit.author.name)
                p.fromJSON(pull_request)
                print("Pull Request:")
                db.session.add(p)
                #print("Hey")
                db.session.commit()
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
                    #line+=1
        #db.session.add(p)
        db.session.commit()
        #print(p.toDict())
        #print(c.toDict())

listen(Comment.__table__,  'after_create', load_file_into_table)
