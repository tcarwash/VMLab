from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import AssignForm, DeleteAssignForm, LoginForm, RegistrationForm, UserEditForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Role, Course, VM
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
    assignform = AssignForm()
    assignform.course.choices=[(course.id, course.course_name) for course in Course.query.all()]
    deleteform = DeleteAssignForm()
    if deleteform.validate_on_submit() and deleteform.delete.data:
        u = User.query.filter(User.id == deleteform.userid.data).one() 
        c = Course.query.filter(Course.id == deleteform.course.data).one()
        u.assignments.remove(c)
        db.session.add(u)
        db.session.commit()
    elif assignform.validate_on_submit() and assignform.submit.data:
        u = User.query.filter(User.id == assignform.userid.data).one() 
        c = Course.query.filter(Course.id == assignform.course.data).one()
        u.assignments.append(c)
        db.session.add(u)
        db.session.commit()
    elif usereditform.validate_on_submit() and usereditform.submit.data:
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
    return render_template('admin.html', usereditform=usereditform, deleteform=deleteform, assignform=assignform, users=users, title='Admin Page')

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

def db_init():
    db.session.add(Role(name='student'))
    db.session.add(Role(name='teacher'))
    db.session.add(VM(vm_name='TestVM', vm_desc='Ubuntu Probably'))
    db.session.commit()
    vmid = VM.query.filter(VM.vm_name=='TestVM').first().id
    print(vmid)
    db.session.add(Course(course_name="Test Course", course_desc='Learn something, probably', vm_id=vmid))
    db.session.commit()

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
        user = User.query.filter(User.username==form.username.data).first()
        print(user.id)
        if user.id == 1:
            db.session.add(Role(name='admin'))
            db.session.commit()
            user.roles.append(Role.query.filter(Role.name=='admin').first())
            db.session.add(user)
            db.session.commit()
            db_init()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
