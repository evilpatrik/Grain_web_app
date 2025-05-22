from flask import render_template, request, redirect, url_for, session, flash,jsonify
from database import UserCRUD, db
from database.models import User
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

@auth.route('/api/verify-user', methods=['POST'])
def verify_user():
    data = request.get_json()
    user = User.query.filter_by(
        national_id=data['nationalId'],
        username=data['username']
    ).first()

    if user:
        session['verified_user'] = user.username  
        return jsonify({'success': True})

    return jsonify({'success': False}), 400


@auth.route('/api/reset-password', methods=['POST'])
def reset_password():
    username = session.get('verified_user')
    if not username:
        return jsonify({'error': 'دسترسی غیرمجاز یا زمان اعتبار گذشته است'}), 400

    data = request.get_json()
    new_password = data.get('newPassword')

    if not new_password:
        return jsonify({'error': 'رمز عبور جدید الزامی است'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'کاربر یافت نشد'}), 404

    try:
        user.set_password(new_password)
        db.session.commit()
        session.pop('verified_user')  # One-time use
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
