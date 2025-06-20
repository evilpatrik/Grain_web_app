from database.crud import ProductCRUD
from database.models import Order, Product
from flask import jsonify, request, send_file
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
@login_required
@role_required('employee')
def get_employee_products():
    sort = request.args.get('sort')
    products = ProductCRUD.get_all_products(sort)
    return jsonify([product.to_dict() for product in products])


@dashboard.route('/api/employee/products/search')
@login_required
@role_required('employee')
def search_products():
    query = request.args.get('q', '')
    products = ProductCRUD.search_products_by_name(query)
    return jsonify([product.to_dict() for product in products])


@dashboard.route('/api/employee/products/<int:product_id>/buy', methods=['POST'])
@login_required
@role_required('employee')
def buy_product(product_id):
    data = request.get_json()
    try:
        quantity = int(data.get('quantity'))
        price = float(data.get('price'))
    except (TypeError, ValueError):
        return jsonify({'message': 'مقدار یا قیمت نامعتبر است'}), 400

    product = ProductCRUD.get_product_by_id(product_id)
    if not product:
        return jsonify({'message': 'محصول یافت نشد'}), 404

    ProductCRUD.increase_quantity(product_id, quantity, price)

    new_order = Order(
        name=product.name,
        quantity=quantity,
        price=price,
        types='buy'
    )
    new_order.calculate_total_price()
    
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'خرید با موفقیت ثبت شد'}), 201


@dashboard.route('/api/emplyee/product/new-buy', methods=['POST']) 
@login_required
@role_required('employee')
def new_buy():
    """ایجاد محصول جدید و ثبت سفارش خرید آن"""
    data = request.get_json()
    
    try:
        name = data.get('name')
        quantity = int(data.get('quantity', 0))
        price = float(data.get('price', 0.0))
    except (TypeError, ValueError):
        return jsonify({'error': 'قیمت یا تعداد نامعتبر است'}), 400

    if not name or quantity <= 0 or price <= 0:
        return jsonify({
            'error': 'نام، تعداد (بزرگ‌تر از صفر) و قیمت (بزرگ‌تر از صفر) الزامی هستند'
        }), 400

    try:
        ProductCRUD.create_product(name, price, quantity)
        
        new_order = Order(
            name=name,
            quantity=quantity,
            price=price,
            types='buy'
        )
        new_order.calculate_total_price()
        db.session.add(new_order)
        db.session.commit()

        return jsonify({'message': 'محصول و سفارش با موفقیت ثبت شد'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'خطا در ثبت محصول و سفارش: {str(e)}'}), 500


@dashboard.route('/api/employee/products/<int:product_id>/sell', methods=['POST'])
@login_required
@role_required('employee')
def sell_product(product_id):
    data = request.get_json()
    try:
        quantity = int(data.get('quantity'))
    except (TypeError, ValueError):
        return jsonify({'message': 'مقدار نامعتبر است'}), 400

    product = ProductCRUD.get_product_by_id(product_id)
    if not product:
        return jsonify({'message': 'محصول یافت نشد'}), 404

    if product.quantity < quantity:
        return jsonify({'message': 'موجودی کافی نیست'}), 400

    ProductCRUD.decrease_quantity(product_id, quantity)

    new_order = Order(
        name=product.name,
        quantity=quantity,
        price=product.price,
        types='sell'
    )
    new_order.calculate_total_price()
    
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'فروش با موفقیت ثبت شد'}), 201
