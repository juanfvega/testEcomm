from sqlalchemy import Boolean, Column, ForeignKey, Table, Integer, String, Float
from sqlalchemy.orm import relationship, declarative_base
from .database import Base


# Make the declrativeMeta
Base = declarative_base()



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    carts = relationship('Carts', back_populates='user')
    orders = relationship('Orders', back_populates='user')


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    category = Column(String)
    cart = relationship('Carts', secondary='cart_products', back_populates='products')
    orders = relationship('Orders', secondary="order_products", back_populates='products')
    inventory = relationship('Inventory', back_populates='product')

class Carts(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='carts')
    products = relationship('Products', secondary='cart_products', back_populates='cart')


#declare Classes/Tables
# Many to Many relationship
cart_products = Table('cart_products', Base.metadata,
                      Column('cart_id', ForeignKey('carts.id'), primary_key=True),
                      Column('product_id', ForeignKey('products.id'), primary_key=True)
                      )



class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    total_amount = Column(Float)
    payment_status = Column(String)
    created_at = String
    user = relationship('User', back_populates='orders')
    products = relationship('Products', secondary='order_products', back_populates='orders')


order_product = Table('order_products', Base.metadata,
                      Column('product_id', ForeignKey('products.id'), primary_key=True),
                      Column('order_id', ForeignKey('orders.id'), primary_key=True))


class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    mov_type = Column(String)
    description = Column(String)
    created_at = Column(String)
    product = relationship('Products', back_populates='inventory')