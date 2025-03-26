from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, User
from functools import wraps

auth = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please login first.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'manager':
            flash('Manager access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'manager':
            flash('Manager access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            session['role'] = user.role
            flash(f'Welcome back, {username}!', 'success')
            
            if user.role == 'admin':
                return redirect(url_for('auth.admin_dashboard'))
            elif user.role == 'manager':
                return redirect(url_for('auth.manager_dashboard'))
            else:
                return redirect(url_for('auth.employee_dashboard'))
        else:
            flash('نام کاربری یا رمز عبور اشتباه است', 'danger')

    return render_template('login.html')

@auth.route('/register_manager', methods=['POST'])
@login_required
@admin_required
def register_manager():
    username = request.form['username']
    password = request.form['password']

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('Username already exists!', 'danger')
        return redirect(url_for('auth.admin_dashboard'))

    db.session.commit()
    
    flash('Manager registered successfully!', 'success')
    return redirect(url_for('auth.admin_dashboard'))

@auth.route('/register_employee', methods=['POST'])
@login_required
@manager_required
def register_employee():
    username = request.form['username']
    password = request.form['password']

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('Username already exists!', 'danger')
        return redirect(url_for('auth.manager_dashboard'))

    new_user = User(username=username, role='employee')
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    flash('Employee registered successfully!', 'success')
    return redirect(url_for('auth.manager_dashboard'))

@auth.route('/admin_dashboard')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

@auth.route('/manager_dashboard')
@login_required
@manager_required
def manager_dashboard():
    return render_template('manager_dashboard.html')

@auth.route('/employee_dashboard')
@login_required
def employee_dashboard():
    if session['role'] != 'employee':
        flash('Access denied.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('employee_dashboard.html')

@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/view_users')
@login_required
@admin_required
def view_users():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username, 'role': user.role} for user in users]
    return render_template('view_users.html', users=users_list)
