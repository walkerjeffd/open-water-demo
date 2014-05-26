from . import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from flask import current_app, request, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_wtf.file import FileField, FileAllowed, FileRequired

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    datasets = db.relationship('Dataset', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def __repr__(self):
        return '<User %r>' % self.email

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    datasets = db.relationship('Dataset', backref='project', lazy='dynamic')

    def __repr__(self):
        return '<Project %s>' % self.name

class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    datasets = db.relationship('Dataset', backref='location', lazy='dynamic')

    def __repr__(self):
        return '<Location %s>' % self.name

class Parameter(db.Model):
    __tablename__ = 'parameters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    units = db.Column(db.String(16), unique=True)
    description = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Parameter %s (%s)>' % (self.name, self.units)

class Dataset(db.Model):
    __tablename__ = 'datasets'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    source_filename = db.Column(db.String(128))
    file_url = db.Column(db.String(128))
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    values = db.relationship('Value', backref='dataset', lazy='dynamic')
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Dataset %d>' % (self.id)

class Value(db.Model):
    __tablename__ = 'values'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime())
    value = db.Column(db.Float)
    parameter_id = db.Column(db.Integer, db.ForeignKey('parameters.id'))
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
