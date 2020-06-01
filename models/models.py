from app import db

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(80),nullable = False,unique = True)
    password = db.Column(db.String(80),nullable = False)
    polls = db.relationship('Polls',backref = 'owner',cascade = "all, delete-orphan")
    voter = db.relationship('Pollvote',foreign_keys = 'Pollvote.user_id',backref = 'user',cascade = "all, delete-orphan")
    def __str__(self):
        return f'{self.id} {self.username} {self.password}'

    def has_voted_poll(self, poll):
        return Pollvote.query.filter(Pollvote.user_id == self.id,Pollvote.poll_id == poll.id).count() > 0

class Polls(db.Model):
    __tablename__ = 'polls'
    id = db.Column(db.Integer,primary_key = True)
    question = db.Column(db.Text,nullable = False)
    choice1 = db.Column(db.String(50),nullable = False)
    choice2 = db.Column(db.String(50),nullable = False)
    selected = db.Column(db.String(50),default = None)
    choice1_total = db.Column(db.Integer,nullable = False,default = 0)
    choice2_total = db.Column(db.Integer,nullable = False,default = 0)
    owner_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def __str__(self):
        return f'{self.id} {self.question} {self.choice1} {self.choice2}'

    def sum(self):
        return sum({self.choice1_total}),sum({self.choice2_total})
class Pollvote(db.Model):
    __tablename__ = 'pollvote'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    poll_id = db.Column(db.Integer,db.ForeignKey('polls.id'))