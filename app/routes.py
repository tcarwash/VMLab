from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, UserEditForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Role
from werkzeug.urls import url_parse


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title='Home')
    
@app.route('/courses', methods=['GET'])
@login_required
def courses():
    return render_template('courses.html', title='Your Courses')

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    usereditform = UserEditForm()
    if usereditform.validate_on_submit():
        u = User.query.filter(User.id == usereditform.userid.data).one()
        if usereditform.admin.data == True and not u.is_admin():
            u.roles.append(Role.query.filter(Role.name == 'admin').one())
        if usereditform.admin.data == False and u.is_admin():
            u.roles.remove(Role.query.filter(Role.name == 'admin').one())
        if usereditform.student.data == True and not u.is_student():
            u.roles.append(Role.query.filter(Role.name == 'student').one())
        if usereditform.student.data == False and u.is_admin():
            u.roles.remove(Role.query.filter(Role.name == 'student').one())
        db.session.add(u)
        db.session.commit()
    users = User.query.all()
    return render_template('admin.html', usereditform=usereditform, users=users, title='Admin Page')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            if any(role.name=='admin' for role in current_user.roles):
                next_page = url_for('admin')
            elif any(role.name=='student' for role in current_user.roles):
                next_page = url_for('courses')
            else:
                next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
