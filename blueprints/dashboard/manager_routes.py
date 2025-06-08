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
        return jsonify({'error': 'نام کاربری قبلاً ثبت شده است'}), 400
    if UserCRUD.get_user_by_national_id(national_id):
        return jsonify({'error': 'کد ملی قبلاً ثبت شده است'}), 400
    if UserCRUD.get_user_by_phone(phone):
        return jsonify({'error': 'شماره تلفن قبلاً ثبت شده است'}), 400

    try:
        if not phone or len(phone) != 11 or not phone.isdigit():
            return jsonify({'error': 'شماره تلفن باید ۱۱ رقم باشد'}), 400

        if not national_id or len(national_id) != 10 or not national_id.isdigit():
            return jsonify({'error': 'کد ملی باید ۱۰ رقم باشد'}), 400

        if not password or len(password) < 8 or password.isalpha() or password.isdigit():
            return jsonify({'error': 'رمز عبور باید حداقل ۸ کاراکتر و شامل حروف و اعداد باشد'}), 400

    except Exception as e:
        return jsonify({'error': f'خطا در پردازش اطلاعات: {str(e)}'}), 400

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

    return jsonify({'message': 'کارمند با موفقیت ثبت شد'}), 201


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
        return jsonify({'success': True, 'deleted_id': employee_id, 'message': 'کارمند با موفقیت حذف شد'})
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
    return jsonify({'message': 'اطلاعات کارمند با موفقیت بروزرسانی شد'}), 201


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
        product_dicts = [{}]

    csv_data = generate_csv(product_dicts, fieldnames=product_dicts[0].keys())

    memory_file = BytesIO()
    with ZipFile(memory_file, 'w') as zipf:
        zipf.writestr('products_backup.csv', csv_data)
        try:
            with open('database/models.py', 'r') as f:
                zipf.writestr('database/models.py', f.read())

            with open('requirements.txt', 'r') as f:
                zipf.writestr('requirements.txt', f.read())

            with open('app.py', 'r') as f:
                zipf.writestr('app.py', f.read())
        except FileNotFoundError as e:
            print(f"هشدار: فایل یافت نشد - {str(e)}")

    memory_file.seek(0)
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='پشتیبان_محصولات.zip'
    )


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
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='پشتیبان_سفارشات.zip'
    )


