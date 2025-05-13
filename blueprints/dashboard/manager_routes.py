from database.crud import UserCRUD
from flask import jsonify,request
from blueprints.dashboard import dashboard
from database import db
from dashboard.routes import login_required, role_required  

@dashboard.route('/api/manager/employees', methods=['GET'])
@login_required
@role_required('manager')
def get_all_employees():
    employees = UserCRUD.get_employee()
    return jsonify(employees)


@dashboard.route('/api/manager/employees', methods=['DELETE'])
@login_required
@role_required('manager')
def delete_selected_employees():
    data = request.get_json()
    ids = data.get('employee_ids', [])

    if not ids:
        return jsonify({'error': 'No employee IDs provided'}), 400

    deleted_ids = []
    for emp_id in ids:
        user = UserCRUD.get_user_by_id(emp_id)
        if user and user.role == 'employee':
            UserCRUD.delete_user(emp_id)
            deleted_ids.append(emp_id)

    return jsonify({
        'success': True,
        'deleted_ids': deleted_ids
    })

