from sqlalchemy import Column

from sqlalchemy import ForeignKey
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import or_
from sqlalchemy import (String,DateTime,Date,Time)

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import with_polymorphic
from sqlalchemy.sql.expression import false, select, true
from sqlalchemy.sql.sqltypes import Boolean
from DbController import Base,session
from sqlalchemy.schema import UniqueConstraint
#from Lessons import Lesson
#from Rooms import Weight_Room
#from Users import User


#JOINED TABLE INHERITANCE

class Reservation(Base):

    __tablename__='Reservations'
 

    id = Column("id",Integer, primary_key=True)     
    is_weight=Column(Boolean)
    user = Column(Integer,ForeignKey("Users.id"),nullable=False)
    

    user_obj=relationship("User",back_populates="reservations_obj")

    __mapper_args__={
      'polymorphic_on':is_weight,     
    }



class Weight_Room_Reservation(Reservation):

        __tablename__='Weight_Room_Reservations'  
          
        id = Column(Integer,ForeignKey(Reservation.id),primary_key=True)
        
        weight_room = Column(Integer,ForeignKey("Weight_Rooms.id"),nullable=False)
        reservation_slot=Column(Integer,ForeignKey("Reservation_slots.id"),nullable=false)

        reservation_slot_obj=relationship("Reservation_Slot",back_populates="weight_reservations_obj")
        weight_room_obj=relationship("Weight_Room",back_populates="weight_reservations_obj")    

        

        def __init__(self,weight_room,reservation_slot,user):
            self.reservation_slot=reservation_slot
            self.weight_room=weight_room
            self.user=user
 


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
        'polymorphic_identity':True,
     
     
     
    }

class Course_Reservation(Reservation):

        __tablename__='Course_Reservations'
      
        id = Column(Integer,ForeignKey(Reservation.id),primary_key=True)
        lesson = Column(Integer,ForeignKey("Lessons.id"),nullable=False)

        lesson_obj=relationship("Lesson",back_populates="course_reservations_obj")    

        def __init__(self,lesson,user):
            self.lesson=lesson
            self.user=user
         
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
        'polymorphic_identity':False,
      
    }





