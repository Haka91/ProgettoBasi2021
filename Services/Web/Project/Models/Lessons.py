from flask.helpers import flash
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from DbController import Base,session




class Lesson(Base):

    __tablename__='Lessons'
   

    id = Column("id",Integer, primary_key=True)
    reservation_slot=Column(Integer,ForeignKey("Reservation_slots.id"),nullable=False) 
    course = Column(Integer,ForeignKey("Courses.id"),nullable=False)   
    course_room = Column(Integer,ForeignKey("Course_Rooms.id"),nullable=False)


    course_room_obj=relationship("Course_Room",back_populates="lessons_obj")
    course_obj =  relationship("Course",back_populates="lessons_obj")
   
    reservation_slot_obj=relationship("Reservation_Slot",back_populates="lessons_obj")
    course_reservations_obj=relationship("Course_Reservation",back_populates="lesson_obj", cascade="all, delete")
    
    #con questo vincolo rendiamo impossibile la prenotazione di un corso nella stessa stanza di un altro nel caso
    #2 trainer aprissero in contemporanea la pagina per prenotare le lezioni
    __table_args__ = (UniqueConstraint('reservation_slot', 'course_room', name='singlelessoninaroom'),
                     )
    
    def __init__(self,reservation_slot,course,course_room):
        self.reservation_slot=reservation_slot
        self.course=course
       
        self.course_room=course_room


    def add_obj(self):

        try:
            session.add(self)
            session.commit()
            return True
        except Exception as e:
            flash(e)
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

    #se ci sono prenotazioni in questa lezione non posso cancellarla
    def is_deletable(self):
       
        return len(self.course_reservations_obj)==0

    #ritorno il numero di prenotazioni
    def reservations(self):
        return len(self.course_reservations_obj)


    #controllo se lo slot è libero
    def lessonSlotFree(self):        
       
        return self.course_obj.maxcostumers>len(self.course_reservations_obj)
        
    #torna la lista degli iscritti alla lezione
    def reservationsUsers(self):
        listOfUsers=list()
        for courseReservation in self.course_reservations_obj:
           listOfUsers.append(courseReservation.user_obj)
        tupleOfUsers=tuple(listOfUsers)
        return tupleOfUsers

    

   