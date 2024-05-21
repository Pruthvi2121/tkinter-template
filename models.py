from sqlalchemy import create_engine, Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, unique=True)
    product_name = Column(Enum("basket", "chokalate", "Basket small", "other"))
    MRP = Column(Integer)
    Damagequantity = Column(Integer)
    sale = Column(Integer)
    Total = Column(Integer)
    type = Column(Enum("ice-cream", "chocolate"))

engine = create_engine('sqlite:///products.db')
Base.metadata.create_all(engine)
