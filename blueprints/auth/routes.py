from flask import render_template, request, redirect, url_for, session, flash,jsonify
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

@auth.route('/api/register_manager', methods=['POST'])
@login_required
@role_required('admin')
def api_register_manager():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    new_user = User(username=username, role='manager')
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Manager registered successfully'}), 201

@auth.route('/api/register_employee', methods=['POST'])
@login_required
@role_required('manager')
def api_register_employee():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    new_user = User(username=username, role='employee')
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Employee registered successfully'}), 201

@auth.route('/api/users', methods=['GET'])
@login_required
@role_required('admin')
def api_view_users():
    users = User.query.all()
    return jsonify([
        {'id': u.id, 'username': u.username, 'role': u.role}
        for u in users
    ])