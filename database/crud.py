from .models import db, Product,User

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

