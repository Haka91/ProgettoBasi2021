from datetime import date, timedelta
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import (DateTime,Date)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import CheckConstraint
from DbController import Base,session
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

    #relationship ORM
    reservation_slots_obj=relationship("Reservation_Slot",back_populates="day_obj", cascade="all, delete")
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
            if(self.break_time is not None and self.opening>=self.break_time ):
                flash("Orario di break precedente ad apertura")
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
             #questo errore lo vediamo solo lato admin se mai dovesse succedere,possiamo considerare il manager un utente "sicuro" per mostrargli errori specifici
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
                #questo errore lo vediamo solo lato admin se mai dovesse succedere,possiamo considerare il manager un utente "sicuro" per mostrargli errori specifici
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

    def reservationsInDay(self):
        totalReservations=0
        for reservationSlot in self.reservation_slots_obj:
            totalReservations=totalReservations+ len( reservationSlot.weight_reservations_obj )
            for lessons in reservationSlot.lessons_obj:
                totalReservations=totalReservations+ len(lessons.course_reservations_obj)
        return totalReservations


