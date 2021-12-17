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
from DbController import Base,session



class Reservation_Slot(Base):

    __tablename__='Reservation_slots'
  

    id = Column("id",Integer,primary_key=True)
    slot_time =Column(Time,nullable=False)
    #non fa riferimento alla Pk di days,ma ad una colonna unique,questo ci evita un passaggio in più nelle query orm per il controllo della data
    day = Column(Date,ForeignKey("Days.date"),nullable=False)

    lessons_obj=relationship("Lesson",back_populates="reservation_slot_obj", cascade="all, delete")
    weight_reservations_obj=relationship("Weight_Room_Reservation",back_populates="reservation_slot_obj", cascade="all, delete")
    day_obj=relationship("Day", back_populates="reservation_slots_obj")


    def __init__(self,slot_time,day):
        self.slot_time=slot_time
        self.day=day

    #lo uso per capire se uno slot è libero per le prenotazioni della sala pesi specifica
    def slotFull(self,maxPrenotations,idRoom):
        totalPrenotation=0
        for weightreservation in self.weight_reservations_obj:
            if weightreservation.weight_room==idRoom:
                totalPrenotation+=1
        return maxPrenotations>=totalPrenotation
    
    #ritorna il numero di slot ancora liberi
    def prenotationOnSlotforRoom(self,idRoom):
        totalPrenotation=0
        for weightreservation in self.weight_reservations_obj:
            if weightreservation.weight_room==idRoom:
                totalPrenotation+=1
        return totalPrenotation

    def prenotationOnSlot(self):    
        return len(self.weight_reservations_obj)
        
    def add_obj(self):

        try:
            session.add(self)
            #non aggiungo direttamente da qui il reservation slot perchè li aggiungo da Day
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


  