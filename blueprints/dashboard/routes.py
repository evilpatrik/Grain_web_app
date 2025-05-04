from flask import render_template, session, redirect, url_for, flash
from . import dashboard
from functools import wraps

# Optional: move these decorators to a shared module
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('لطفا ابتدا وارد شوید', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('role') != required_role:
                flash('دسترسی کافی ندارید', 'danger')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@dashboard.route('/admin_dashboard')
@login_required
@role_required('admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@dashboard.route('/manager_dashboard')
@login_required
@role_required('manager')
def manager_dashboard():
    return render_template('manager_dashboard.html')

@dashboard.route('/employee_dashboard')
@login_required
@role_required('employee')
def employee_dashboard():
    return render_template('employee_dashboard.html')
