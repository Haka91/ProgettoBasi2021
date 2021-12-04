from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import or_
from sqlalchemy import (String,DateTime,Date,Time)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import with_polymorphic
from sqlalchemy.sql.schema import CheckConstraint
from DbController import Base,engine
from Models.Reservation_Slots import Reservation_slot





class Day(Base):

    __tablename__='Days'    

    date = Column(Date,primary_key=True)
    opening=Column(DateTime,nullable=False)
    closing=Column(DateTime,nullable=False)
    break_time =Column(Time)
    break_slot =Column(Integer,CheckConstraint('break_slot>0'),CheckConstraint('break_slot<47'),nullable=False)
  
    reservation_slots_obj=relationship("Reservation_slot",back_populates="day_obj")
     
    def add_obj(self):

        try:
            engine.session.add(self)
            engine.session.commit()
            return True
        except Exception as e:
            print(e)
            engine.session.rollback()
            return False

    def delete_obj(self):
       
        try:
            engine.session.delete(self)
            engine.session.commit()
            return True
        except:
            engine.session.rollback()
            return False

    def update_obj(self, date ,opening,closing,break_time,break_slot):
        try:            
            self.opening = opening         
            self.closing =closing
            self.break_time=break_time
            self.break_slot=break_slot  
            engine.session.commit()
            return True
        except:
            engine.session.rollback()
            return False

