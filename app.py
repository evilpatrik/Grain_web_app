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

# Login route
@app.route('/')
def home():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
