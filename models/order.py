from sqlalchemy import Column, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship, backref

from models.book import Books
from data_base.dbcore import Base



class Order(Base):

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    data = Column(DateTime)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer)
    data = Column(Text)
    products = relationship(
        Books,
        backref=backref('orders',
                        uselist=True,
                        cascade='delete,all'))


    def __repr__(self):
        return f"{self.quantity} {self.data}"
