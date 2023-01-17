from ..db.db import SqlAlchemyBase 
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String 

class Review(SqlAlchemyBase):
    __tablename__ = 'reviews' 

    review_id = Column(String, nullable=False, primary_key=True)
    author_id = Column(String, nullable=False)
    order_id = Column(String, nullable=False) 
    grade = Column(Integer, nullable=False) 
    comment = Column(String, nullable=False) 

    def get_feedback_data_as_dict(self):
        """
        Converts review data dict type 
        :return: dict {
            'review_id': str,
            'author': str,
            'order_id': str,
            'grade': int,
            'comment': str
        }
        """
        order_data = {
            'review_id': self.review_id,
            'author': self.author,
            'order_id': self.order_id,
            'grade': self.grade,
            'comment': self.comment
        }
        return order_data
    
