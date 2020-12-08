from datetime import datetime
from hashlib import md5
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

follow = db.Table(
    'follow',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    admin = db.Column(db.Boolean, default=False)

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    teams = db.relationship('Team', secondary=follow, backref=db.backref('fans', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    nickname = db.Column(db.String)
    hq = db.Column(db.String)
    logo = db.Column(db.String)
    about = db.Column(db.String)
    
    teams = db.relationship('Team', backref='conference', lazy='dynamic')

    def __repr__(self):
        return f'<Conference {self.name}>'


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String)
    mascot = db.Column(db.String)
    abbr = db.Column(db.String)
    about = db.Column(db.String)
    logo = db.Column(db.String)
    conference_id = db.Column(db.Integer, db.ForeignKey('conference.id'))

    posts = db.relationship('Post', backref='team_page', lazy='dynamic')

    def __repr__(self):
        return f'<Conference {self.school}>'

