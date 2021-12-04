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
from DbController import Base,engine




class Lesson(Base):

    __tablename__='Lessons'
   

    id = Column("id",Integer, primary_key=True)
    reservation_slot_occupied = Column(Integer,nullable=False)
    start_time =Column(Time,nullable=False)
    course = Column(Integer,ForeignKey("Courses.id"),nullable=False)
    trainer = Column(Integer,ForeignKey("Users.id"),nullable=False)



    course_obj =  relationship("Course",back_populates="lessons_obj")
    trainer_obj= relationship("User", back_populates="lessons_obj")

    course_reservations_obj=relationship("Course_Reservations",back_populates="lesson_obj")
    
    

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

    def update_obj(self, reservation_slot_occupied ,start_time,course,trainer):
        try:
            self.reservation_slot_occupied=reservation_slot_occupied
            self.start_time = start_time         
            self.course =course
            self.trainer=trainer           
            engine.session.commit()
            return True
        except:
            engine.session.rollback()
            return False