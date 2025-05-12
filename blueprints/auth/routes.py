from flask import render_template, request, redirect, url_for, session, flash,jsonify
from database import UserCRUD, db
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
        user = UserCRUD.get_user_by_username(username)

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
    name = data.get('name')
    family = data.get('family')
    phone = data.get('phone')
    national_id = data.get('national_id')
    username = data.get('username')
    password = data.get('password')

    if UserCRUD.get_user_by_username(username):
        return jsonify({'error': 'Username already exists'}), 400

    new_user = UserCRUD(username=username, role='manager', name=name, family=family, phone=phone, national_id=national_id)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Manager registered successfully'}), 201

@auth.route('/api/register_employee', methods=['POST'])
@login_required
@role_required('manager')
def api_register_employee():
    data = request.get_json()
    name = data.get('name')
    family = data.get('family')
    phone = data.get('phone')
    national_id = data.get('national_id')
    username = data.get('username')
    password = data.get('password')

    if UserCRUD.get_user_by_username(username):
        return jsonify({'error': 'Username already exists'}), 400

    new_user = UserCRUD(username=username, role='employee', name=name, family=family, phone=phone, national_id=national_id)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Employee registered successfully'}), 201

@auth.route('/api/users', methods=['GET'])
@login_required
@role_required('admin')
def api_view_users():
    users = UserCRUD.get_all_users()
    return jsonify([u.to_dict() for u in users])