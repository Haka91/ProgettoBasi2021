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
from app import Base,engine





class Days(Base):

    __tablename__='Days'    

    date = Column(Date,primary_key=True)
    opening=Column(DateTime,nullable=False)
    closing=Column(DateTime,nullable=False)
    break_time =Column(Time)
    break_slot =Column(Integer,CheckConstraint('break_slot>0'),CheckConstraint('break_slot<47'),nullable=False)
  

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

  
