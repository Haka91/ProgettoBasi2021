from sqlalchemy import Column
from datetime import date, timedelta
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import CheckConstraint
from DbController import Base,session
from flask.helpers import flash



class Policy(Base):

    __tablename__='Policies'   

    id = Column("id",Integer, primary_key=True)
    name = Column(String(50),nullable=False,unique=True)
    room_percent=Column(Integer,CheckConstraint('room_percent<101'),CheckConstraint('room_percent>0'),nullable=False,default=100)
    max_user_reserv=Column(Integer,CheckConstraint('max_user_reserv>0'),CheckConstraint('max_user_reserv<49'),nullable=False,default=48)

    #relationship ORM
    days_obj=relationship("Day",back_populates="policy_obj", cascade="all, delete")  
   
    def __init__(self,name,room_percent,max_user_reserv):
        self.name=name
        self.room_percent=room_percent
        self.max_user_reserv=max_user_reserv


    def add_obj(self):

        try:
            session.add(self)
            session.commit()
            return True
        except Exception as e:
            if " duplicate key value violates unique constraint" in e.__str__():
                flash("Policy già esistente nel DB")
                session.rollback()
                return False
            else:
                flash("impossibile aggiungere policy,hai controllato i campi?")   
            session.rollback()
            return False

    def delete_obj(self):
       
        try:
            session.delete(self)
            session.commit()
            return True
        except Exception as e:
            flash(e)   
            print(e) 
            session.rollback()
            return False

    
    def is_deletable(self):

        if(len(self.days_obj)==0):
            return True
        else:
            for day in self.days_obj:
                #se la policy ha giorni puù vecchi di 30 gg allora posso cancellarla
                if(day.date>(date.today()-timedelta(days=30))):            
                    for reservationSlot in day.reservation_slots_obj:
                        if (len(reservationSlot.lessons_obj)>0 or len(reservationSlot.weight_reservations_obj)>0):
                            return False
            return True

            