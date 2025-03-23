from flask import Blueprint, render_template, session, redirect, url_for

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
def dashboard_view():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    if session['role'] == 'manager':
        return render_template('manager_dashboard.html', username=session['username'])
    else:
        return render_template('employee_dashboard.html', username=session['username'])
