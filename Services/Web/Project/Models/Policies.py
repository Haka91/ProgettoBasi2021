from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import or_
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import with_polymorphic
from sqlalchemy.sql.schema import CheckConstraint
from DbController import Base,session



class Policy(Base):

    __tablename__='Policies'
   

    id = Column("id",Integer, primary_key=True)
    name = Column(String(50))
    room_percent=Column(Integer,CheckConstraint('room_percent<101'),CheckConstraint('room_percent>0'),nullable=False,default=100)
    max_user_reserv=Column(Integer,CheckConstraint('max_user_reserv>0'),CheckConstraint('max_user_reserv<49'),nullable=False,default=48)

    days_obj=relationship("Day",back_populates="policy_obj")
  
   
    def __init__(self,name,room_percent,max_user_reserv):
        self.name=name
        self.room_percent=room_percent
        self.max_user_reserv=max_user_reserv


    def add_obj(self):

        try:
            session.add(self)
            session.commit()
            return True
        except Exception as e:
            print(e)
            session.rollback()
            return False

    def delete_obj(self):
       
        try:
            session.delete(self)
            session.commit()
            return True
        except:
            session.rollback()
            return False


    def update_obj(self, name ,room_percent,max_user_reserv):
        try:
            self.name=name
            self.room_percent = room_percent        
            self.max_user_reserv =max_user_reserv      
            session.commit()
            return True
        except:
            session.rollback()
            return False