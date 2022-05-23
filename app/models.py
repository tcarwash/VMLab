from app import db, app, login 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import backref


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

assignment = db.Table('assignment', 
    db.Column('user', db.Integer, db.ForeignKey('User.id')),
    db.Column('course', db.Integer, db.ForeignKey('Course.id'))
    )

user_instance = db.Table('user_instance',
    db.Column('user', db.Integer, db.ForeignKey('User.id')),
    db.Column('instance', db.Integer, db.ForeignKey('Instance.id'))
    )

user_role = db.Table('user_role',
    db.Column('user', db.Integer, db.ForeignKey('User.id')),
    db.Column('role', db.Integer, db.ForeignKey('Role.id'))
    )

class Role(db.Model):
    __tablename__ = 'Role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)
    
class VM(db.Model):
    __tablename__ = 'VM'
    id = db.Column(db.Integer, primary_key=True)
    vm_name = db.Column(db.String(32), index=True, unique=True)
    vm_desc = db.Column(db.String(120), index=True)
    path = db.Column(db.String(64), index=True)

class Course(db.Model):
    __tablename__ = 'Course'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(32), index=True, unique=True)
    course_desc = db.Column(db.String(120), index=True)
    course_text = db.Column(db.Text(4294000000))
    vm_id = db.Column(db.Integer, db.ForeignKey('VM.id'))
    users = db.relationship('User', secondary=assignment)

    def __repr__(self):
        return '<Course {}>'.format(self.course_name)

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))
    assignments = db.relationship('Course', secondary=assignment)
    roles = db.relationship('Role', secondary=user_role)
    instances = db.relationship('Instance', backref=backref("users", cascade="all,delete"), secondary=user_instance)

    def is_admin(self):
        return any(role.name=='admin' for role in self.roles)

    def is_student(self):
        return any(role.name=='student' for role in self.roles)
        
    def is_teacher(self):
        return any(role.name=='teacher' for role in self.roles)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<username {}>'.format(self.username)


class Instance(db.Model):
    __tablename__ = 'Instance'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.id'))
    url = db.Column(db.String(32), unique=True)
    course = db.relationship("Course", backref=backref('instances', cascade="all,delete"))
    vm = db.relationship("VM", backref=backref('instances', cascade="all,delete"), secondary=Course.__table__, primaryjoin="Instance.course_id == Course.id", secondaryjoin="Course.vm_id == VM.id")
