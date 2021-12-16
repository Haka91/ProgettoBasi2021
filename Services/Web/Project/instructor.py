# Blueprint per la sezione user

from flask import Flask, request
from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for
from flask_login.utils import login_required
from flask.helpers import url_for
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import true
from DbController import session
from flask_login import current_user
from Models.Courses import Course
from Models.Lessons import Lesson
from Models.Rooms import Room, Course_Room
from Models.Users import User,at_least_trainer_required
from Models.Reservation_Slots import Reservation_Slot




instructor = Blueprint('instructor',__name__,url_prefix='/instructor')

# Introduction page
@instructor.route('/introduzione')
@login_required
@at_least_trainer_required
def introduzione():
    corsi=session.query(Course).filter_by(trainer=current_user.id).all() 
    lezioni=session.query(Lesson).all() #FILTRARE SOLO PER LE LEZIONI DEI CORSI CHE FA L'ISTRUTTORE NELLA PROSSIMA SETTIMANA (O NEI PROSSIMI GIORNI) 
    return render_template('/Instructor/introduzione.html',lezioni=lezioni,corsi=corsi) 


# Page where the next lessons are listed
@instructor.route('/prossimeLezioni')
@login_required
@at_least_trainer_required
def prossimeLezioni():
    #lezioni=session.query(Lesson).filter().all() #FILTRARE SOLO PER LE LEZIONI CHE L'ISTRUTTORE FARA' DA OGGI IN POI
    courses=current_user.courses_obj
    print(courses)
    lessonlist=list()
    for course in courses:             
        for lesson in course.lessons_obj:
            #prendo le lezioni della settimana
            if(lesson.reservation_slot_obj.day>=(datetime.today().date())and lesson.reservation_slot_obj.day<=((datetime.today()+timedelta(days=7)).date())):          
             lessonlist.append(lesson)
    lessontuple=tuple(lessonlist)
    return render_template('/Instructor/prossimeLezioni.html',lezioni=lessontuple) 


# Page to create new lessons of an existing course
@instructor.route('/creaLezioni')
@login_required
@at_least_trainer_required
def creaLezioni():    
    tableVisible=''' hidden="hidden" ''' #now the table is NOT visible
    formVisible='''  ''' # now the form is visible
    corsi=session.query(Course).all()
    stanze=session.query(Course_Room).all()
  
 
    corsi=session.query(Course).all() #FILTRARE SOLO I CORSI INSEGNATI DALL'ISTRUTTORE
    rooms=session.query(Room).all()  
    lessonsSameDaySameRoom=session.query(Lesson).filter(Lesson.course_room==1).all()
    
    
    listOfSlotOccupied=list()
    for lesson in lessonsSameDaySameRoom:
        print(lesson.reservation_slot_obj)
        listOfSlotOccupied.append(lesson.reservation_slot_obj)
    
    return render_template('/Instructor/creaLezioni.html',tableVisible=tableVisible,formVisible=formVisible,corsi=corsi,stanze=stanze)


# Function called once the "Cerca" button is called. After that it finds the slots available in the room, date and duration required
# in the form above, and prints all the different options available. It also saves the data submitted by the user in the form and it repopulates it again
@instructor.route('/inserisciLezioni', methods = ['POST', 'GET'])
@login_required
@at_least_trainer_required
def inserisciLezioni():
    tableVisible='''  ''' #now the table will be visible
    formVisible=''' hidden="hidden" ''' # now the form is NOT visible
    # retrieve the data from the form and prepare a string to print all of the info on the page
    corso = request.form["course"]
    #data = request.form["date"]
    dove = request.form["chooseroom"]
    slot = request.form["slots"]
    titleTable = "Slot prenotabili"
    slots=session.query(Reservation_Slot).filter(Reservation_Slot.day == (datetime.today().date())).all()
    #titleTable ="Slot prenotabili per il corso: "+corso+", data: "+data+", dove: "+dove+", slot: "+slot+"."
    return render_template('/Instructor/creaLezioni.html',tableVisible=tableVisible,formVisible=formVisible,titleTable=titleTable,corso=corso,dove=dove,slot=slots)


# function to create a lesson for a specified course in a specified slot of time (all specified before)
@instructor.route('/reserveSlot/<int:idSlot>,<int:idCorso>,<int:idRoom>')
@login_required
@at_least_trainer_required
def reserveSlot(idSlot,idCorso,idRoom):
    
    tempLesson=Lesson(idSlot,idCorso,idRoom)
    tempLesson.add_obj()
    return redirect(url_for('instructor.creaLezioni'))