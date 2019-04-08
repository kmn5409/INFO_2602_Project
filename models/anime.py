from sqlalchemy import Column, String, Integer, Float
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
    author_name = Column(String(50))
    commit_message = Column(String(5000))
    commit_comment = Column(String(5000))
    types = Column(String(10))
    sha = Column(String(50))
    
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

    def fromJSON(self, json_rec,types):
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
        if(types == "commit"):
            self.author_name = json_rec.commit.author.name
            self.commit_message = json_rec.commit.message[:]
            self.types = "commit"
            self.sha = json_rec.commit.sha
        elif(types == "comment"):
            self.author_name = json_rec.user.name
            self.commit_comment = json_rec.body
            self.types = "comment"
            self.sha = json_rec.html_url

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
        if(self.types == "commit"):
            repre.update({
                'id':self.id,
                'author_name':self.author_name,
                'commit_message' : self.commit_message,
                'type':self.types,
                'sha': self.sha               
            })
        elif(self.types == "comment"):
            repre.update({
                'id':self.id,
                'author_name':self.author_name,
                'commit_comment' : self.commit_comment,
                'type':self.types,
                'sha': self.sha              
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



def load_pkfile_into_table(target, connection, **kw):
    import json
    g = Github("c5c1fb044b46cde5a102ae0f507309e01f68d593")
    for repo in g.get_user("kmn5409").get_repos():
        if(repo.name == "Test"):
            for i in repo.get_commits():
                #print("Message: ",i.commit.message[:])
                p = Anime()
                #print(i)
                #print(i.commit.author.name)
                p.fromJSON(i,"commit")
                db.session.add(p)
            for j in repo.get_comments():
                print("Comments: \n\n",j.body)
                p = Anime()
                #print(i)
                #print(i.commit.author.name)
                p.fromJSON(j,"comment")
                db.session.add(p)
        #db.session.add(p)
        db.session.commit()
    


#listen(Pokemon.__table__, 'after_create', load_pkfile_into_table)
listen(Anime.__table__, 'after_create', load_pkfile_into_table)