from flask import render_template, request, redirect, url_for, session, flash
from models import db, User
from functools import wraps
from . import auth

# Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('لطفا ابتدا وارد شوید', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                flash('دسترسی لازم را ندارید', 'danger')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['username'] = username
            session['role'] = user.role
            flash(f'Welcome, {username}!', 'success')

            return redirect(url_for(f'dashboard.{user.role}_dashboard'))
        else:
            flash('نام کاربری یا رمز اشتباه است', 'danger')

    return render_template('login.html')

# Logout
@auth.route('/logout')
def logout():
    session.clear()
    flash('با موفقیت خارج شدید', 'info')
    return redirect(url_for('auth.login'))

# Admin register manager
@auth.route('/register_manager', methods=['POST'])
@login_required
@role_required('admin')
def register_manager():
    username = request.form['username']
    password = request.form['password']

    if User.query.filter_by(username=username).first():
        flash('نام کاربری قبلاً ثبت شده است', 'danger')
        return redirect(url_for('dashboard.admin_dashboard'))

    new_user = User(username=username, role='manager')
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    flash('مدیر ثبت شد', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))

# Manager register employee
@auth.route('/register_employee', methods=['POST'])
@login_required
@role_required('manager')
def register_employee():
    username = request.form['username']
    password = request.form['password']

    if User.query.filter_by(username=username).first():
        flash('نام کاربری قبلاً ثبت شده است', 'danger')
        return redirect(url_for('dashboard.manager_dashboard'))

    new_user = User(username=username, role='employee')
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    flash('کارمند ثبت شد', 'success')
    return redirect(url_for('dashboard.manager_dashboard'))

# View all users (admin)
@auth.route('/view_users')
@login_required
@role_required('admin')
def view_users():
    users = User.query.all()
    return render_template('view_users.html', users=users)
