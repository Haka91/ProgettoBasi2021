from datetime import date, datetime, timedelta
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
from sqlalchemy.sql.schema import CheckConstraint
from sqlalchemy.sql.type_api import NULLTYPE
from DbController import Base,session
from Models.Reservation_Slots import Reservation_Slot
from flask.helpers import flash




class Day(Base):

    __tablename__='Days'    
    id=Column(Integer,primary_key=True)
    date = Column(Date,nullable=False,unique=True)
    opening=Column(DateTime,nullable=False)
    closing=Column(DateTime,nullable=False)
    break_time =Column(DateTime,nullable=True)
    break_slot =Column(Integer,CheckConstraint('break_slot>=0'),CheckConstraint('break_slot<47'),nullable=False,default=0)
    policy=Column(Integer,ForeignKey("Policies.id"),nullable=False,default=1)

  
    reservation_slots_obj=relationship("Reservation_Slot",back_populates="day_obj")
    policy_obj=relationship("Policy",back_populates="days_obj")
     

    def __init__(self,date,opening,closing,break_slot,policy=1,break_time=None):
        self.date=date
        self.opening=opening
        self.closing=closing
        self.break_time=break_time
        self.break_slot=break_slot
        self.policy=policy
 
    def add_obj(self):
        from Models.Reservation_Slots import Reservation_Slot
        try:
            if(self.opening>=self.closing):
                flash("Orario di chiusura precedente a apertura")
                return False
                      
            session.add(self)            
            guard=True
            startTime=self.opening
            #creo per ogni giorno i relativi timeslot
            while(startTime<=self.closing and guard):
                if(self.break_time==None ):                    
                    tempReservation=Reservation_Slot(startTime,self.date)
                    #se ci sono errori cancello il commit della sessione
                    guard=tempReservation.add_obj()
                    startTime=startTime + timedelta(minutes=30)
                elif((self.break_time + timedelta(minutes=(self.break_slot*30)))<self.closing):
                      #controllo che la pausa non sia più lunga della chiusura,nel caso cancello tutto
                     while(startTime<=self.closing and guard):                        
                       
                        if(startTime<self.break_time or startTime>(self.break_time +timedelta(minutes=(self.break_slot*30)))):
                                tempReservation=Reservation_Slot(startTime,self.date)
                                guard=tempReservation.add_obj()

                         
                        startTime=startTime + timedelta(minutes=30)
                else:
                    flash("break più lungo dell'apertura della palestra")
                    session.rollback()
                    return False                
            
            session.commit()
            return True
        except Exception as e:
            
            if " duplicate key value violates unique constraint" in e.__str__():
                flash("Uno o piu' giorno già esistenti nel DB")
            else:
                flash(e)
            session.rollback()
            return False

    def delete_obj(self):
        if(self.is_deletable):

            try:
                session.delete(self)
                session.commit()
                return True
            except Exception as e:
                flash(e)
                session.rollback()
                return False
        else:
            flash("non puoi cancellare questo giorno")


    def is_deletable(self):

        if(self.date<(date.today()-timedelta(days=30))):
            return True
        else:            
            for reservationSlot in self.reservation_slots_obj:
                if (len(reservationSlot.lessons_obj)>0 or len(reservationSlot.weight_reservations_obj)>0):
                    return False
            return True

