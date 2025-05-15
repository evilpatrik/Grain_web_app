from database.crud import UserCRUD
from flask import jsonify,request,send_file
from blueprints.dashboard import dashboard
from database import db
from blueprints.dashboard.routes import login_required, role_required  
from database.crud import ProductCRUD
from io import BytesIO, StringIO
from zipfile import ZipFile
import csv

@dashboard.route('/api/manager/register-employee', methods=['POST'])
@login_required
@role_required('manager')
def register_employee():
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
        role='employee',
    )
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Employee registered successfully'}), 201


@dashboard.route('/api/manager/employees', methods=['GET'])
@login_required
@role_required('manager')
def get_all_employees():
    employees = UserCRUD.get_employee()
    return jsonify(employees)


@dashboard.route('/api/manager/employees/<int:employee_id>', methods=['DELETE'])
@login_required
@role_required('manager')
def delete_employee(employee_id):
    user = UserCRUD.get_user_by_id(employee_id)
    if user and user.role == 'employee':
        UserCRUD.delete_user(employee_id)
        return jsonify({'success': True, 'deleted_id': employee_id})
    return jsonify({'error': 'کارمند یافت نشد'}), 404

@dashboard.route('/api/manager/employees/<int:employee_id>', methods=['PUT'])
@login_required
@role_required('manager')
def update_employee(employee_id):
    data = request.get_json()
    user = UserCRUD.get_user_by_id(employee_id)
    if not user or user.role != 'employee':
        return jsonify({'error': 'کارمند یافت نشد'}), 404
    
    name = data.get('name')
    family = data.get('family')
    phone = data.get('phone')
    password = data.get('password')
    
    if UserCRUD.get_user_by_phone(phone):
        return jsonify({'error': 'Phone number already exists'}), 400


    user.name = name
    user.family = family
    user.phone = phone
    if password:
        if user.check_password(password):
            return jsonify({'error': 'رمز جدیدی وارد کنید'}), 400
        user.set_password(password)
    

    db.session.commit()
    return jsonify({'message': 'بروزرسانی با موفقیت انجام شد'}),201


@dashboard.route('/api/manager/products', methods=['GET'])
@login_required 
@role_required('manager')
def get_all_products():
    products = ProductCRUD.get_all_products()
    product_dicts = [p.to_dict() for p in products]
    return jsonify(product_dicts)

