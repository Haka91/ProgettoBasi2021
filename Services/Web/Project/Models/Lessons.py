from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import or_
from sqlalchemy import (String,DateTime,Date,Time)

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import with_polymorphic
from sqlalchemy.sql.expression import false, true

from app import Base,engine


class Lessons(Base):

    __tablename__='Lessons'
   

    id = Column("id",Integer, primary_key=True)
    reservation_slot_occupied = Column(Integer,nullable=False)
    start_time =Column(Time,nullable=False)
    

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
