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
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.sqltypes import Boolean
from app import Base,engine


class Rooms(Base):
    __tablename__='Rooms'


    id = Column("id",Integer, primary_key=True)
    name = Column(String(50),nullable=False)
    description=Column(String(200),nullable=False)
    max_capacity=Column(Integer,nullable=False)
    is_weight=Column(Boolean)

    __mapper_args__={
      
      'polymorphic_on':is_weight
    }

class Weight_Room(Rooms):

    __tablename__='Weight_Rooms'   
         
    id = Column(Integer,ForeignKey(Rooms.id),primary_key=True)

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
    __mapper_args__ = {
     
        'polymorphic_identity':True
    }

class Course_Room(Rooms):

    __tablename__='Course_Rooms' 
        
    id = Column(Integer,ForeignKey(Rooms.id),primary_key=True)      
    __mapper_args__ = {
       
        'polymorphic_identity':False
    }