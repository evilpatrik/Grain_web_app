from .models import db, Product,User,Order

class ProductCRUD:
    @staticmethod
    def create_product(name, price, quantity=0):
        new_product = Product(name=name, price=price, quantity=quantity)
        db.session.add(new_product)
        db.session.commit()
        return new_product

    @staticmethod
    def get_all_products():
        return Product.query.all()

    @staticmethod
    def get_product_by_id(product_id):
        return Product.query.get(product_id)

    @staticmethod
    def update_product(product_id, **kwargs):
        product = Product.query.get(product_id)
        if not product:
            return None
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        db.session.commit()
        return product

    @staticmethod
    def delete_product(product_id):
        product = Product.query.get(product_id)
        if not product:
            return False
        db.session.delete(product)
        db.session.commit()
        return True
    
    @staticmethod
    def decrease_quantity(product_id, quantity):
        product = Product.query.get(product_id)
        if not product or product.quantity < quantity:
            return False
        product.quantity -= quantity
        db.session.commit()
        return True

    @staticmethod
    def increase_quantity(product_id, quantity, price):
        product = Product.query.get(product_id)
        if not product:
            return False
        product.quantity += quantity
        product.price = price  # Update the price each time
        db.session.commit()
        return True

    @staticmethod
    def search_products_by_name(query):
        return Product.query.filter(Product.name.ilike(f"%{query}%")).all()

class UserCRUD:
    @staticmethod
    def create_user(username, password, role, name, family, phone, national_id):
        new_user = User(username=username, role=role, name=name, family=family, phone=phone, national_id=national_id)
        new_user.set_password(password)  # Use set_password to hash and set the password
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_user_by_phone(phone):
        return User.query.filter_by(phone=phone).first()
    
    @staticmethod
    def get_employee():
        employees = User.query.filter_by(role = 'employee').all()
        return [
            {
                'id': user.id,
                'name': user.name,
                'family': user.family,
                'username': user.username,
                'phone': user.phone,
                'role': user.role
            }
            for user in employees
        ]
    
    @staticmethod
    def get_manager():
        managers =User.query.filter_by(role='manager').all()
        return [
            {
                'id': user.id,
                'name': user.name,
                'family': user.family,
                'username': user.username,
                'phone': user.phone,
                'role': user.role
            }
            for user in managers
        ]
    
    @staticmethod
    def get_all_users():
        users = User.query.all()
        return [
            {
                'id': user.id,
                'name': user.name,
                'family': user.family,
                'username': user.username,
                'phone': user.phone,
                'role': user.role
            }
            for user in users
        ]

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return False
        db.session.delete(user)
        db.session.commit()
        return True
    
    @staticmethod
    def get_user_by_national_id(national_id):
        return User.query.filter_by(national_id=national_id).first()
    
    @staticmethod
    def update_user(user_id, **kwargs):
        user = UserCRUD.get_user_by_id(user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return user

class OrderCRUD ():
    @staticmethod
    def create_order(name, price, quantity, types, time):
        new_order = Order(
            name=name,
            price=price,
            quantity=quantity,
            types=types,
            time=time,
        )
        new_order.total_price(price, quantity)
        db.session.add(new_order)
        db.session.commit()
        return new_order
    
    
    @staticmethod
    def delete_order(order_id):
        order = Order.query.get(order_id)
        if not order:
            return False
        db.session.delete(order)
        db.session.commit()
        return True
    
    @staticmethod
    def get_order_by_id(order_id):
        return Order.query.get(order_id)

    @staticmethod
    def get_order_by_name(name):
        return Order.query.filter_by(name=name).first()

    @staticmethod
    def get_all_orders():
        return Order.query.all()
    
