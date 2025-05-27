from database.crud import UserCRUD,ProductCRUD
from database.models import Order
from flask import jsonify,request,send_file
from blueprints.dashboard import dashboard
from database import db
from blueprints.dashboard.routes import login_required, role_required  
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

        try:
        # Validate phone number
        if not phone or len(phone) != 11 or not phone.isdigit():
            return jsonify({'error': 'Phone number must be exactly 11 digits'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 400

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


    user.name = name
    user.family = family
    user.phone = phone
    if password:
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

def generate_csv(data_list, fieldnames):
    csv_buffer = StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data_list)
    return csv_buffer.getvalue()

@dashboard.route('/api/manager/orders', methods=['GET'])
@login_required
@role_required('manager')
def get_manager_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders])


@dashboard.route('/api/manager/backup/product')
@login_required
@role_required('manager')
def backup_product():
    products = ProductCRUD.get_all_products()
    product_dicts = [p.to_dict() for p in products]
    if not product_dicts:
        product_dicts = [{}]  # Avoid crash on empty list

    csv_data = generate_csv(product_dicts, fieldnames=product_dicts[0].keys())

    memory_file = BytesIO()
    with ZipFile(memory_file, 'w') as zipf:
        zipf.writestr('products_backup.csv', csv_data)

    memory_file.seek(0)
    return send_file(memory_file, mimetype='application/zip', as_attachment=True,
                     download_name='product_backup.zip')

@dashboard.route('/api/manager/backup/order')
@login_required
@role_required('manager')
def backup_order():
    orders = Order.query.all()
    order_dicts = [o.to_dict() for o in orders]
    if not order_dicts:
        order_dicts = [{}]

    csv_data = generate_csv(order_dicts, fieldnames=order_dicts[0].keys())

    memory_file = BytesIO()
    with ZipFile(memory_file, 'w') as zipf:
        zipf.writestr('orders_backup.csv', csv_data)

    memory_file.seek(0)
    return send_file(memory_file, mimetype='application/zip', as_attachment=True,
                     download_name='order_backup.zip')