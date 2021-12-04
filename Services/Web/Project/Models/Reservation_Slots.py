from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import or_
from sqlalchemy import (String,DateTime,Date,Time)


from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import with_polymorphic
from sqlalchemy.sql.expression import false
from DbController import Base,engine



class Reservation_slot(Base):

    __tablename__='Reservation_slots'
  

    id = Column("id",Integer,primary_key=True)
    slot_time =Column(Time,nullable=False)
    day = Column(Date,ForeignKey("Days.date"),nullable=False)

    day_obj=relationship("Day", back_populates="reservation_slots_obj")

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

    def update_obj(self, slot_time,day):
        try:
            self.slot_time=slot_time 
            self.day=day       
            engine.session.commit()
            return True
        except:
            engine.session.rollback()
            return False
  