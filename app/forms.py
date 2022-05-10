from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, HiddenField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User, Role, Course

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UserEditForm(FlaskForm):
    userid = HiddenField('UserID')
    admin = BooleanField('Admin')
    student = BooleanField('Student')
    teacher = BooleanField('Teacher')
    submit = SubmitField('Submit Changes')
    
class CourseForm(FlaskForm):
    course_name = StringField('Course Name', validators=[DataRequired()])
    course_desc = StringField('Descrtiption')
    course_text = StringField('Body', validators=[DataRequired()])
    vm = SelectField('VM')
    submit = SubmitField('Submit')

class DeleteAssignForm(FlaskForm):
    userid = HiddenField("UserID")
    course = HiddenField("CourseID")
    delete = SubmitField("Remove Course")

class AssignForm(FlaskForm):
    userid = HiddenField('UserID')
    course = SelectField('Add Course', validators=[DataRequired()])
    submit = SubmitField('Add Course')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
