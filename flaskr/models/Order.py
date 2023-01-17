from ..db.db import SqlAlchemyBase 
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime 

from ..middleware import auth_middleware

class Order(SqlAlchemyBase):
    __tablename__ = 'orders' 

    order_id = Column(String, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String) 
    address_from = Column(String, nullable=False) 
    address_to = Column(String, nullable=False) 
    created_by = Column(String, nullable=False) 
    assigned_to = Column(String) 
    time_start = Column(DateTime, nullable=False)
    time_finish = Column(DateTime, nullable=False)
    completed = Column(Integer, nullable=False) 

    def get_order_data_as_dict(self):
        """
        Converts order data dict type 
        :return: dict {
            'order_id': str
            'title': str
            'description': str
            'username': str
            'adderss_from': str
            'adderss_tp': str
            'completed': int 
        }
        """
        order_data = {
            'order_id': self.order_id,
            'title': self.title,
            'description': self.description,
            'address_from': self.address_from,
            'address_to': self.address_to,
            'created_by': self.created_by,
            'assigned_to': self.assigned_to,
            'time_start': self.time_start,
            'time_finish': self.time_finish,
            'completed': self.completed,
        }
        return order_data
    
