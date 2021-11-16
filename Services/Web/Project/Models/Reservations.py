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
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.sqltypes import Boolean
from app import Base,engine


class Reservations(Base):

    __tablename__='Reservations'
 

    id = Column("id",Integer, primary_key=True)     
    is_weight=Column(Boolean)
    user = Column(Integer,ForeignKey("Users.id"),nullable=False)
    #reservation_slot = Column(Integer,ForeignKey("Reservation_Slots.id"),nullable=False)

    __mapper_args__={
      'polymorphic_on':is_weight,
     
    }

class Weight_Room_Reservations(Reservations):

        __tablename__='Weight_Room_Reservations'  
          
        id = Column(Integer,ForeignKey(Reservations.id),primary_key=True)

        weight_room = Column(Integer,ForeignKey("Weight_Rooms.id"),nullable=False)
        
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
        'polymorphic_identity':True,
     
     
     
    }

class Course_Reservations(Reservations):

        __tablename__='Course_Reservations'
      
        id = Column(Integer,ForeignKey(Reservations.id),primary_key=True)

        lesson = Column(Integer,ForeignKey("Lessons.id"),nullable=False)


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
        'polymorphic_identity':False,
      
    }





