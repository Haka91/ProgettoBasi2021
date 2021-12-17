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
from DbController import Base,session
#from Models.Reservations import Weight_Room_Reservations



#JOINED TABLE INHERITANCE
class Room(Base):
    __tablename__='Rooms'


    id = Column("id",Integer, primary_key=True)
    name = Column(String(50),nullable=False)
    description=Column(String(200),nullable=False)
    max_capacity=Column(Integer,nullable=False)
    is_weight=Column(Boolean)

    __mapper_args__={
      
      'polymorphic_on':is_weight
    }

class Weight_Room(Room):

    __tablename__='Weight_Rooms'   
         
    id = Column(Integer,ForeignKey(Room.id),primary_key=True)

    weight_reservations_obj=relationship("Weight_Room_Reservation" ,back_populates="weight_room_obj",cascade="all, delete")

    def __init__(self,name,description,max_capacity):
        self.name=name
        self.description=description
        self.max_capacity=max_capacity

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
    __mapper_args__ = {
     
        'polymorphic_identity':True
    }

class Course_Room(Room):

    __tablename__='Course_Rooms' 
        
    id = Column(Integer,ForeignKey(Room.id),primary_key=True)  

    lessons_obj=relationship("Lesson",back_populates="course_room_obj",cascade="all, delete")
 

    def __init__(self,name,description,max_capacity):
        self.name=name
        self.description=description
        self.max_capacity=max_capacity  

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
    __mapper_args__ = {
       
        'polymorphic_identity':False
    }
