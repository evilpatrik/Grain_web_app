from database.crud import ProductCRUD
from database.models import Order
from flask import jsonify,request,send_file
from blueprints.dashboard import dashboard
from database import db
from blueprints.dashboard.routes import login_required, role_required  


@dashboard.route('/api/employee/orders', methods=['GET'])
@login_required
@role_required('employee')
def get_employee_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders])

@dashboard.route('/api/employee/products', methods=['GET'])
def get_employee_products():
    products = ProductCRUD.get_all_products()
    return jsonify([product.to_dict() for product in products])

