
from datetime import datetime, timedelta
from sqlalchemy import (Column,ForeignKey,Integer,String)
from sqlalchemy.orm import relationship
from DbController import Base,session
from flask_login import UserMixin,current_user
from werkzeug.utils import redirect
from functools import wraps
from flask.helpers import url_for,flash
from app import bcrypt,login_manager






class User(UserMixin,Base):

    __tablename__='Users'
  

    id = Column("id",Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column( String(50), nullable=False)
    email = Column(String(40), nullable=False,unique=True)
    cellular=Column(String(40), nullable=False)
    address = Column( String(30), nullable=False)
    city = Column(String(30), nullable=False)
    password = Column( String, nullable=False)    
    role = Column(Integer,ForeignKey("Roles.id"),nullable=False,default=3)
     
  

    role_obj=relationship("Role",back_populates="users_obj")

    courses_obj=relationship("Course",back_populates="trainer_obj",cascade="all, delete")
    reservations_obj=relationship("Reservation",back_populates="user_obj",cascade="all, delete")



    def __init__(self,name,surname,email,cellular,address,city,password,role):
        self.name=name
        self.surname=surname
        self.email=email 
        self.cellular=cellular
        self.address=address
        self.city=city
        self.password=bcrypt.generate_password_hash(password).decode("utf-8")
        self.role=role
        

    def checkpsw(self, password):
        return bcrypt.check_password_hash(self.password, password)

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


    def update_obj(self,name,surname,cellular,address,city):
        try:          
            
            self.name=name 
            self.surname=surname                
            self.cellular=cellular
            self.address=address
            self.city=city             
            session.commit()
            return True
        
        except:
            session.rollback()
            return False


    def update_password(self,old_password,new_password):
        try:
            if(self.checkpsw(old_password)):
                self.password=bcrypt.generate_password_hash(new_password).decode("utf-8")
                session.commit()
                return True
            else:
                return False

        except:
            session.rollback()
            return False

    def update_role(self,role):
        try:
            self.role=role
            session.commit()
            return True
        except:            
            session.rollback()
            return False


    def get_role(self):
        try:
            return self.role
        except:
            
            return 0

    def contactTracing(self):
        #lo dichiaro nella funzione per evitare un possibile circular input
        from Models.Reservations import Weight_Room_Reservation
        usersListWithDuplicates=list()
        #mi aggiungo per essere sicuro di essere nella lista da rimuovere alla fine
        usersListWithDuplicates.append(self)
        for reservation in self.reservations_obj:
            if(reservation.is_weight):
               #recupero tutte le prenotazioni fatte nello stesso slot,nella stessa ora,nella stessa stanza,tra 7 giorni fa e ieri
               reservationsForRoomAndSlot= session.query(Weight_Room_Reservation).filter(Weight_Room_Reservation.weight_room==reservation.weight_room and Weight_Room_Reservation.reservation_slot==reservation.reservation_slot and Weight_Room_Reservation.reservation_slot_obj.day<datetime.today().date() and Weight_Room_Reservation.reservation_slot_obj.day>(datetime.today()-timedelta(days=7)).date())
               for weightReservation in reservationsForRoomAndSlot:
                  usersListWithDuplicates.append(weightReservation.user_obj)
            else:
                #la lezione è stata fatta tra 7 giorni fa e ieri?
                if reservation.lesson_obj.reservation_slot_obj.day<(datetime.today().date()) and reservation.lesson_obj.reservation_slot_obj.day>(datetime.today()-timedelta(days=7)).date() :
                    #anche il trainer viene a contatto quindi lo riprendo dal corso della lezione
                    usersListWithDuplicates.append(reservation.lesson_obj.course_obj.trainer_obj)
                    for courseReservation in reservation.lesson_obj.course_reservations_obj:
                        usersListWithDuplicates.append(courseReservation.user_obj)
        #un utente potrebbe essere un trainer oppure potrebbe essere stato un trainer ed ora è uno user,controllo se ha mai tenuto corsi(l'impossibilità di cancellare i corsi prima di 30 gg mi garantisce il ritrovamento di essi)
        for course in self.courses_obj:
            for lesson in course.lessons_obj:
                #lezione tenuta tra 7 giorni fa e ieri?
                if lesson.reservation_slot_obj.day<(datetime.today().date()) and lesson.reservation_slot_obj.day>(datetime.today()-timedelta(days=7)).date() :
                    for personalCourseReservation in lesson.course_reservations_obj:
                        usersListWithDuplicates.append(personalCourseReservation.user_obj)

        #ora ho una lista piena di duplicati probabilmente che sistemo con il set __eq__ ed __hash__ sono già integrati da flask ed sqlalchemy
        
        userlistWithNoDuplicate=list(set(usersListWithDuplicates))
        #rimuovo me stesso dai miei contatti       
        userlistWithNoDuplicate.remove(self)             
        
        return tuple(userlistWithNoDuplicate)
        
    def soonReservations(self):
        reservationList=list()
        for reservation in  self.reservations_obj:
            if(reservation.is_weight):
                if reservation.reservation_slot_obj.day<(datetime.today()+timedelta(days=4)).date() and reservation.reservation_slot_obj.day>(datetime.today().date()) :
                  reservationList.append(reservation)
            else:
                if reservation.lesson_obj.reservation_slot_obj.day<(datetime.today()+timedelta(days=4)).date() and reservation.lesson_obj.reservation_slot_obj.day>(datetime.today().date()):
                    reservationList.append(reservation)
        return tuple(reservationList)
        
#metodo richiesto da FLASK-LOGIN 

@login_manager.user_loader
def load_user(id_user):
    try:
        return session.query(User).get(id_user)       
    except:
        None





#dobbiamo inserire qui le funzioni per evitare i circular import
#qui forzo la selezione della Role uguale all'admin,se creassimo una nuova role avrebbe più' poteri di admin 
def at_least_manager_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_anonymous:
            if current_user.get_role() == 3 :
                return f(*args, **kwargs)
            else:
                flash("ERROR 404 PAGE NOT FOUND","error")

                return redirect(url_for("general.index"))
        else:
            flash("ERROR 404 PAGE NOT FOUND","error")
            return redirect(url_for("general.index"))

    return wrapper





def at_least_trainer_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_anonymous:
            if current_user.get_role() >= 2:
                return f(*args, **kwargs)
            else:
                flash("ERROR 404 PAGE NOT FOUND","error")
                return redirect(url_for("general.index"))
        else:
            flash("ERROR 404 PAGE NOT FOUND","error")
            return redirect(url_for("general.index"))

    return wrapper




def at_least_user_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_anonymous:
            if current_user.get_role() >= 1:
                return f(*args, **kwargs)
            else:
                flash("ERROR 404 PAGE NOT FOUND","error") 
                return redirect(url_for("general.index"))
        else:
            flash("ERROR 404 PAGE NOT FOUND","error") 
            return redirect(url_for("general.index"))

    return wrapper