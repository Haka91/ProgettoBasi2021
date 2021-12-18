from sqlalchemy import Column
from datetime import date, timedelta
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import (String)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean
from DbController import Base,session
from flask.helpers import flash




#JOINED TABLE INHERITANCE
class Room(Base):
    __tablename__='Rooms'


    id = Column("id",Integer, primary_key=True)
    name = Column(String(50),nullable=False)
    description=Column(String(200),nullable=False)
    max_capacity=Column(Integer,nullable=False)
    is_weight=Column(Boolean)
    isvisible = Column(Boolean,default=True)

    #funzione generica per nascondere o rendere visibile sala
    def activate_or_deactivate_obj(self):
        
            try:
                self.isvisible=not self.isvisible            
                session.commit()
                return True
            except:
                session.rollback()
                return False
        

    __mapper_args__={
      
      'polymorphic_on':is_weight
    }

class Weight_Room(Room):

    __tablename__='Weight_Rooms'   
         
    id = Column(Integer,ForeignKey(Room.id),primary_key=True)

    weight_reservations_obj=relationship("Weight_Room_Reservation" ,back_populates="weight_room_obj",cascade="all, delete")

    def __init__(self,name,description,max_capacity,isVisible=True):
        self.name=name
        self.description=description
        self.max_capacity=max_capacity
        self.isvisible=isVisible

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


    def is_deletable(self):
        deletable=True
        if(len(self.weight_reservations_obj)==0):
            return deletable
        else:
            #se le prenotazioni sono più vecchie di 30 giorni posso cancellarle
            for weightReserations in self.weight_reservations_obj:
               if( weightReserations.reservation_slot_obj.day >(date.today()- timedelta(days=30))):
                   deletable=False
        return deletable

    __mapper_args__ = {
     
        'polymorphic_identity':True
    }

class Course_Room(Room):

    __tablename__='Course_Rooms' 
        
    id = Column(Integer,ForeignKey(Room.id),primary_key=True)  

    lessons_obj=relationship("Lesson",back_populates="course_room_obj",cascade="all, delete")
 

    def __init__(self,name,description,max_capacity,isVisible=True):
        self.name=name
        self.description=description
        self.max_capacity=max_capacity
        self.isvisible=isVisible  

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

    def is_deletable(self):
        deletable=True
        if(len(self.lessons_obj)==0):
            return deletable
        else:
            #se le lezioni sono più vecchie di 30 giorni posso cancellarle
            for lesson in self.lessons_obj:
               if( lesson.reservation_slot_obj.day >(date.today()- timedelta(days=30))):
                   deletable=False
        return deletable

    __mapper_args__ = {
       
        'polymorphic_identity':False
    }
