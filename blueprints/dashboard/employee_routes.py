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

@dashboard.route('/api/employee/products/<int:product_id>/buy', methods=['POST'])
def buy_product(product_id):
    data = request.get_json()
    quantity = data.get('quantity')
    price = data.get('price')

    product = ProductCRUD.get_product_by_id(product_id)

    new_order = Order(
        name=product.name,
        quantity=quantity,
        price=price,
        types='buy'
    )
    new_order.total_price(price,quantity)

    db.session.add(new_order)
    product.price = price 
    db.session.commit()

    return jsonify({'message': 'سفارش با موفقیت ثبت شد'}), 201