from flask import Flask, render_template
from database import db, bcrypt, UserCRUD
from blueprints.auth import auth
from blueprints.dashboard import dashboard
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'amin-aras-mehran'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grains.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
bcrypt.init_app(app)


app.register_blueprint(auth)
app.register_blueprint(dashboard)

# Create database tables and default admin
with app.app_context():
    db.create_all()
    # Create default admin user if not exists
    admin = UserCRUD.get_user_by_username('admin')
    if not admin:
        admin = UserCRUD.create_user(username='admin',password='admin', role='admin', name='amin', family='kareshi', phone='09051254424', national_id='2920559257')
        admin.set_password('admin')
        db.session.add(admin)
        db.session.commit()

    # Create default manager user if not exists
    manager = UserCRUD.get_user_by_username('manager')
    if not manager:
        manager = UserCRUD.create_user(username='manager', password='manager123', role='manager', name='John', family='Doe', phone='09051254425', national_id='2920559258')
        manager.set_password('manager123')
        db.session.add(manager)
        db.session.commit()

    # Create default employee user if not exists
    employee = UserCRUD.get_user_by_username('employee')
    if not employee:
        employee = UserCRUD.create_user(username='employee', password='employee123', role='employee', name='Jane', family='Smith', phone='09051254426', national_id='2920559259')
        employee.set_password('employee123')
        db.session.add(employee)
        db.session.commit()

# Login route
@app.route('/')
def home():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
