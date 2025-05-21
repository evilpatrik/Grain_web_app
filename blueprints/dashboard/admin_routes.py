import os
import zipfile
import io
from blueprints.dashboard.routes import login_required, role_required
from database import db
from blueprints.dashboard import dashboard
from flask import jsonify,request,send_file
from database.crud import UserCRUD

@dashboard.route('/api/admin/register-manager', methods=['POST'])
@login_required
@role_required('admin')
def register_manager():
    data = request.get_json()
    name = data.get('name')
    family = data.get('family')
    phone = data.get('phone')
    national_id = data.get('national_id')
    username = data.get('username')
    password = data.get('password')

    if UserCRUD.get_user_by_username(username):
        return jsonify({'error': 'Username already exists'}), 400
    if UserCRUD.get_user_by_national_id(national_id):
        return jsonify({'error': 'National ID already exists'}), 400
    if UserCRUD.get_user_by_phone(phone):
        return jsonify({'error': 'Phone number already exists'}), 400

    new_user = UserCRUD.create_user(
        name=name,
        family=family,
        phone=phone,
        national_id=national_id,
        username=username,
        password=password,
        role='manager',
    )
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'manager registered successfully'}), 201

@dashboard.route('/api/admin/backup', methods=['GET'])
@login_required
@role_required('admin')
def backup_project():
    base_dir = os.path.abspath(os.path.dirname(__file__))

    project_root = os.path.abspath(os.path.join(base_dir, '../../'))

    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_root):
            for file in files:
                file_path = os.path.join(root, file)

                if any(excluded in file_path for excluded in ['__pycache__', '.pyc', '.db']):
                    continue

                arcname = os.path.relpath(file_path, project_root)
                zipf.write(file_path, arcname)

    memory_file.seek(0)

    return send_file(
        memory_file,
        mimetype="application/zip",
        as_attachment=True,
        download_name="project_backup.zip"
    )
@dashboard.route('/api/admin/users', methods=['GET'])
@login_required
@role_required('admin')
def api_view_users():
    users = UserCRUD.get_all_users()
    return jsonify([u.to_dict() for u in users])
