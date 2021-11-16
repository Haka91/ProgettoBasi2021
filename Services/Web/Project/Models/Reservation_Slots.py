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
from app import Base,engine




class Reservation_slots(Base):

    __tablename__='Reservation_slots'
  

    id = Column("id",Integer,primary_key=True)
    slot_time =Column(Time,nullable=False)

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

  