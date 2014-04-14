# -*- coding: utf-8 -*-

from app import db
# nécessaire pour la gestion des avatars
from hashlib import md5

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    prevenu = db.Column(db.Boolean, default = False)
    tweeter = db.Column(db.String(40), default = '', unique = True)
    tweet = db.Column(db.Boolean, default = False)
    messages = db.relationship('Message', backref = 'author', lazy = 'dynamic')
    subscriptions = db.relationship('Subscription', backref = 'owner', lazy = 'dynamic')
    about_me = db.Column(db.String(140))
    website = db.Column(db.String(200))
    last_seen = db.Column(db.DateTime)

    def avatar(self, size):
        """Gestion des avatar"""
        return 'http://www.gravatar.com/avatar/'+ md5(self.email).hexdigest() +'?d=mm&s=' + str(size)

    # serie de methodes recquises par Flask-login
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    # Verif l'unicite d'un login
    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname = nickname).first() == None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname = new_nickname).first() == None:
                break
            version += 1
        return new_nickname

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)


# ----------------------------
#   APICLOCK
# ----------------------------

class Subscription(db.Model):
    """Gestion subscription = Abonnement flux PODCAST"""
    __tablename__ = 'subscription'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    imageurl = db.Column(db.String(150))
    description = db.Column(db.String(200))
    copyright = db.Column(db.String(150))
    url = db.Column(db.String(150))
    urlxml = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    podcasts = db.relationship('Podcast', backref = 'partof', lazy = 'dynamic')

    def __repr__(self):
        return "<subscription('%s', '%s', '%s', '%s)>" % \
            (self.name, self.imageurl, self.description, self.url)


class Podcast(db.Model):
    """Gestion podcast"""
    __tablename__ = 'podcast'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    date = db.Column(db.String(50))
    description = db.Column(db.String(200))
    pathfile = db.Column(db.String(150))
    type = db.Column(db.String(50))
    urlweb = db.Column(db.String(150))
    etat = db.Column(db.String(50))
    readstate = db.Column(db.Boolean)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'))

    def __repr__(self):
        return "<podcast('%s', '%s')>" % \
            (self.title, self.description)

db.create_all()