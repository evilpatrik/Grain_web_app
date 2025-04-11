# Import necessary modules and components
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, User
from functools import wraps

# Create a Flask Blueprint for authentication routes
auth = Blueprint('auth', __name__)

# Decorator to ensure user is logged in before accessing a route
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('لطفا ابتدا وارد شوید', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator to restrict access to admin users only
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            flash('دسترسی ادمین نیاز است', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator to restrict access to manager users only
def manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'manager':
            flash('دسترسی مدیر نیاز است', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Login route (GET for form, POST for login attempt)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists in DB and validate password
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # Store session info
            session['username'] = username
            session['role'] = user.role
            flash(f'Welcome back, {username}!', 'success')
            
            # Redirect to the appropriate dashboard
            if user.role == 'admin':
                return redirect(url_for('auth.admin_dashboard'))
            elif user.role == 'manager':
                return redirect(url_for('auth.manager_dashboard'))
            else:
                return redirect(url_for('auth.employee_dashboard'))
        else:
            # Invalid credentials
            flash('نام کاربری یا رمز عبور اشتباه است', 'danger')

    # Render login page
    return render_template('login.html')

# Admin can register a new manager
@auth.route('/register_manager', methods=['POST'])
@login_required
@admin_required
def register_manager():
    username = request.form['username']
    password = request.form['password']

    # Check for existing user
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('نام کاربری وجود دارد', 'danger')
        return redirect(url_for('auth.admin_dashboard'))
    
    # Create and store new manager
    new_user = User(username=username, role='manager')
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    flash('مدیر با موفقیت ثبت شد', 'success')
    return redirect(url_for('auth.admin_dashboard'))

# Manager can register a new employee
@auth.route('/register_employee', methods=['POST'])
@login_required
@manager_required
def register_employee():
    username = request.form['username']
    password = request.form['password']

    # Check for existing user
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('نام کاربری وجود دارد', 'danger')
        return redirect(url_for('auth.manager_dashboard'))

    # Create and store new employee
    new_user = User(username=username, role='employee')
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    flash('کارمند با موفقیت ثبت شد', 'success')
    return redirect(url_for('auth.manager_dashboard'))

# Admin dashboard route
@auth.route('/admin_dashboard')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

# Manager dashboard route
@auth.route('/manager_dashboard')
@login_required
@manager_required
def manager_dashboard():
    return render_template('manager_dashboard.html')

# Employee dashboard route with role check
@auth.route('/employee_dashboard')
@login_required
def employee_dashboard():
    if session['role'] != 'employee':
        flash('Access denied.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('employee_dashboard.html')

# Logout route: clear session
@auth.route('/logout')
def logout():
    session.clear()
    flash('شما خارج شدید', 'info')
    return redirect(url_for('auth.login'))

# Admin can view all registered users
@auth.route('/view_users')
@login_required
@admin_required
def view_users():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username, 'role': user.role} for user in users]
    return render_template('view_users.html', users=users_list)
