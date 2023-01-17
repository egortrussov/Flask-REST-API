from ..db.db import SqlAlchemyBase 
from sqlalchemy import Column, select
from sqlalchemy.sql.sqltypes import Integer, String, JSON 

from ..middleware import auth_middleware

from .Order import Order
from .Review import Review

from ..db.db import create_session

class User(SqlAlchemyBase):
    __tablename__ = 'users' 

    user_id = Column(String, nullable=False, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False) 
    name = Column(String, nullable=False) 
    is_worker = Column(Integer, nullable=False) 

    def get_user_data_as_dict(self):
        """
        Converts data from sqlalchemy response to dict type 
        :return: dict {
            user_id: str,
            username: str,
            name: str,
            is_worker: int
        }
        """
        user_data = {
            'user_id': self.user_id,
            'username': self.username,
            'name': self.name,
            'is_worker': self.is_worker
        }
        return user_data
    
    def check_password_hash(self, password):
        """
        Checks is password is equal to hashed password
        :return: bool
        """
        return auth_middleware.check_password_hash(password, self.password)
    
    def encode_auth_token(self):
        """
        Create auth token 
        :return: str 
        """
        return auth_middleware.encode_auth_token(self.user_id, self.is_worker)
    
    def get_assigned_orders(self):
        """
        Returns array of assigned orders (id, time_start, time_finish)
        :return: array<dict>
        """
        session = create_session() 

        orders = session.query(Order).filter_by(assigned_to=self.user_id).all() 

        res = []

        for order in orders:
            res.append(order.get_order_data_as_dict())
        
        return res
    
    def get_assigned_orders_timestamps(self):
        """
        Returns array of statring and finishing times of orders assigned to the user 
        :return: array<(datetime, datetime)>
        """
        assigned_orders = self.get_assigned_orders() 

        timestamps = list(
            map(
                lambda ordr : (ordr['time_start'], ordr['time_finish']), 
                filter(lambda ordr : not ordr['completed'], assigned_orders)
            )
        )
        
        return timestamps
    
    def get_created_orders(self):
        """
        Returns array of assigned orders (id, time_start, time_finish)
        :return: array<dict>
        """
        session = create_session() 

        orders = session.query(Order).filter_by(created_by=self.user_id).all() 

        res = []

        for order in orders:
            res.append(order.get_order_data_as_dict())
        
        return res
    
    def get_order_grades(self):
        """
        returns list of grades of all orders completed by the user
        """
        session = create_session() 

        reviews = session.query(Order, Review).filter(Order.assigned_to==self.user_id).filter(Order.completed==1).filter(Review.order_id==Order.order_id)

        grades = session.execute(
            select(Review.grade).where(Order.assigned_to==self.user_id).where(Order.completed==1).where(Review.order_id==Order.order_id)
        ).all()

        return list(map(lambda x : x[0], grades))