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
#from Models.Courses import Course
#from Models.Reservations import Course_Reservations
#from Models.Users import User
from DbController import Base,session




class Lesson(Base):

    __tablename__='Lessons'
   

    id = Column("id",Integer, primary_key=True)
    reservation_slot=Column(Integer,ForeignKey("Reservation_slots.id"),nullable=False) 
    course = Column(Integer,ForeignKey("Courses.id"),nullable=False)   
    course_room = Column(Integer,ForeignKey("Course_Rooms.id"),nullable=False)


    course_room_obj=relationship("Course_Room",back_populates="lessons_obj")
    course_obj =  relationship("Course",back_populates="lessons_obj")
   
    reservation_slot_obj=relationship("Reservation_Slot",back_populates="lessons_obj")
    course_reservations_obj=relationship("Course_Reservation",back_populates="lesson_obj")
    
    
    def __init__(self,reservation_slot,course,course_room):
        self.reservation_slot=reservation_slot
        self.course=course
       
        self.course_room=course_room


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

    def update_obj(self, reservation_slot_occupied ,start_time,course,trainer):
        try:
            self.reservation_slot_occupied=reservation_slot_occupied
            self.start_time = start_time         
            self.course =course
            self.trainer=trainer           
            session.commit()
            return True
        except:
            session.rollback()
            return False