from sqlalchemy import Column, String, Integer, Float, DateTime
from models.entity import Entity
from sqlalchemy.event import listen
import csv
from github import Github


from app import db


#https://afternoon-refuge-76633.herokuapp.com/api/pokemon
#https://pacific-mesa-82818.herokuapp.com/ | https://git.heroku.com/pacific-mesa-82818.git
#https://devcenter.heroku.com/articles/git

'''
class Pokemon(Entity, db.Model):
    __tablename__='pokemon'
    name=Column(String(100))
    hp=Column(String(4))
    type_1=Column(String(20))
    type_2=Column(String(20))
    attack=Column(Integer)
    defense=Column(Integer)
    special_attack=Column(Integer)
    special_defense=Column(Integer)
    total=Column(Integer)
    speed=Column(Integer)
'''

class Anime(Entity,db.Model):
    __tablename__ = 'anime'
    #id = Column(Integer,primary_key=True,autoincrement='auto')
    user = Column(String(50))
    repo = Column(String(100))
    author_name = Column(String(50))
    pull_request_message = Column(String(5000))
    pull_request_comment = Column(String(5000))
    types = Column(String(15))
    number = Column(Integer)
    pull_request_id = Column(String(50))
    timestamp = Column(DateTime())
    
    '''
    __tablename__='anime'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    anime_id=Column(Integer)
    name=Column(String(100))
    genre=Column(String(10))
    Type=Column(String(15))
    episodes=Column(Integer)
    rating=Column(Float)
    members=Column(Integer)
    '''

    def __init__(self):
        super().__init__()
        Entity.__init__(self)

    def fromJSON(self, user,name,repo,pull_request,types):
        '''
        if 'name' in json_rec:
            self.name = json_rec['name']
        else:
            raise Exception('The name field is required')

        self.hp = json_rec['hp'] if 'hp' in json_rec else ''
        self.type_1 = json_rec['type_1'] if 'type_1' in json_rec else ''
        self.type_2 = json_rec['type_2'] if 'type_2' in json_rec else ''
        self.attack = json_rec['attack'] if 'attack' in json_rec else 0
        self.defense = json_rec['defense'] if 'defense' in json_rec else 0
        self.special_attack = json_rec['sp_atk'] if 'sp_atk' in json_rec else 0
        self.special_defense= json_rec['sp_def'] if 'sp_def' in json_rec else 0
        self.total = json_rec['total'] if 'total' in json_rec else 0
        self.speed = json_rec['speed'] if 'speed' in json_rec else 0
        '''
        #print("Here ",json_rec.commit.author.name)
        self.user = user
        self.repo = repo
        if(types == "pull_request"):
            self.author_name = pull_request.user.login #Need to verify if this is the author
            self.pull_request_message = pull_request.body
            self.types = types
            self.number = pull_request.number
        elif(types == "comment"):
            self.author_name = pull_request.user.name
            self.commit_comment = pull_request.body
            self.types = "comment"
            self.sha = sha
            self.comment_id = number

    '''
    def toDict(self):
        repre = Entity.toDict(self)
        repre.update({
            'name': self.name,
            'hp':self.hp,
            'type_1':self.type_1,
            'type_2':self.type_2,
            'attack':self.attack,
            'defense':self.defense,
            'special_attack':self.special_attack,
            'special_defense':self.special_defense,
            'total':self.total,
            'speed':self.speed
        })
        return repre
        '''
    def toDict(self):
        repre = Entity.toDict(self)
        if(self.types == "pull_request"):
            repre.update({
                'id':self.id,
                'author_name':self.user,
                'pull_request_message' : self.pull_request_message,
                'type':self.types,               
            })
        elif(self.types == "comment"):
            repre.update({
                'id':self.id,
                'author_name':self.author_name,
                'commit_comment' : self.commit_comment,
                'type':self.types,
                'sha': self.sha,
                'comment_id': self.comment_id              
            })
        return repre
        '''
        return {
            'id':self.id,
            'anime_id': self.anime_id,
            'name': self.name,
            'genre':self.genre,
            'type':self.Type,
            'episodes':self.episodes,
            'rating':self.rating,
            'members':self.members
        }
        '''

#class Comment:
    

def load_pkfile_into_table(target, connection, **kw):
    import json
    g = Github("c5c1fb044b46cde5a102ae0f507309e01f68d593")
    user = "kmn5409"
    name = "Test"
    for repo in g.get_user(user).get_repos():
        if(repo.name == name):
            for pull_request in repo.get_pulls():
                #print("Message: ",i.commit.message[:])
                p = Anime()
                #print(i)
                #print(i.commit.author.name)
                p.fromJSON(user,name,repo.name,pull_request,"pull_request")
                db.session.add(p)
                #GET request
                line = 0
                '''
                for j in i.get_comments():
                    print("Comments: \n\n",j.body)
                    p = Anime()
                    #print(i)
                    #print(i.commit.author.name)
                    p.fromJSON(user,name,j,i.commit.sha,line,"comment")
                    db.session.add(p)
                    line+=1
                '''
        #db.session.add(p)
        db.session.commit()
    


#listen(Pokemon.__table__, 'after_create', load_pkfile_into_table)
listen(Anime.__table__, 'after_create', load_pkfile_into_table)