# Blueprint per la sezione user

from flask import  request
from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for
from flask_login.utils import login_required
from flask.helpers import flash, url_for

from DbController import session
from flask_login import current_user
from Models.Courses import Course
from Models.Lessons import Lesson
from Models.Rooms import Room, Course_Room
from Models.Users import at_least_trainer_required, User
from Models.Reservation_Slots import Reservation_Slot
from Models.Days import Day





instructor = Blueprint('instructor',__name__,url_prefix='/instructor')

# Introduction page
@instructor.route('/introduzione')
@login_required
@at_least_trainer_required
def introduzione():
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    corsi=session.query(Course).filter_by(trainer=current_user.id).all()    
    user=session.query(User).get(current_user.id)  
    courses=current_user.courses_obj    
    lessonlist=list()
    for course in courses:             
        for lesson in course.lessons_obj:
            #prendo le lezioni delle prossime 2 settimane
            if(lesson.reservation_slot_obj.day>=(datetime.today().date())and lesson.reservation_slot_obj.day<=((datetime.today()+timedelta(days=7)).date())):          
             lessonlist.append(lesson)
    lessontuple=tuple(lessonlist)  
    return render_template('/Instructor/introduzione.html',ruolo=user.role,userName=userName,lezioni=lessontuple,corsi=corsi) 


# Page that shows, for a specific course, the list of users booked for the course
@instructor.route('/listaIscrittiLezione/<int:idLezione>,<string:nomeCorso>')
@login_required
@at_least_trainer_required
def listaIscrittiLezione(idLezione,nomeCorso):
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    lesson=session.query(Lesson).get(idLezione)
    #recupero la lista dalla funzione
    utentiIscritti = lesson.reservationsUsers()
    return render_template('/Instructor/listaIscrittiLezione.html',userName=userName,nomeCorso=nomeCorso,utentiIscritti=utentiIscritti)


# Page where the next lessons are listed
@instructor.route('/prossimeLezioni')
@login_required
@at_least_trainer_required
def prossimeLezioni():
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    courses=current_user.courses_obj    
    lessonlist=list()
    for course in courses:             
        for lesson in course.lessons_obj:
            #prendo le lezioni delle prossime 2 settimane
            if(lesson.reservation_slot_obj.day>=(datetime.today().date())and lesson.reservation_slot_obj.day<=((datetime.today()+timedelta(days=14)).date())):          
             lessonlist.append(lesson)
    lessontuple=tuple(lessonlist)
    return render_template('/Instructor/prossimeLezioni.html',userName=userName,lezioni=lessontuple) 


# Page to create new lessons of an existing course
@instructor.route('/creaLezioni')
@login_required
@at_least_trainer_required
def creaLezioni():    
    tableVisible=''' hidden="hidden" ''' #now the table is NOT visible
    formVisible='''  ''' # now the form is visible
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
  
 
    #filtro per le stanze visibili
    stanze=session.query(Course_Room).filter(Course_Room.isvisible).all() 
    courses=current_user.courses_obj   
    

    
    return render_template('/Instructor/creaLezioni.html',userName=userName,tableVisible=tableVisible,formVisible=formVisible,corsi=courses,stanze=stanze)


# Function called once the "Cerca" button is called. After that it finds the slots available in the room, date and duration required
# in the form above, and prints all the different options available. It also saves the data submitted by the user in the form and it repopulates it again
@instructor.route('/inserisciLezioni', methods = ['POST', 'GET'])
@login_required
@at_least_trainer_required
def inserisciLezioni():
    tableVisible='''  ''' #now the table will be visible
    formVisible=''' hidden="hidden" ''' # now the form is NOT visible
    # retrieve the data from the form and prepare a string to print all of the info on the page
   
    try :
        corso = request.form["course"]
        dataString=request.form.get('datalezione')
        dove = int(request.form["chooseroom"])      
        print(dataString)
        data=datetime.strptime(dataString,'%Y-%m-%d')
        
    except :        
        flash("errore nei campi")
        stanze=session.query(Course_Room).filter(Course_Room.isvisible).all()
        courses=current_user.courses_obj
        # string to show in the navbar of the page
        userName = "Ciao "+current_user.name+" ! "
        return render_template('/Instructor/creaLezioni.html',userName=userName,tableVisible=''' hidden="hidden" ''' ,formVisible='''  ''',corsi=courses,stanze=stanze)      

    if(data<=datetime.today()):
        flash("non puoi creare lezioni antecedenti alla data odierna")
        stanze=session.query(Course_Room).filter(Course_Room.isvisible).all()
        courses=current_user.courses_obj
        # string to show in the navbar of the page
        userName = "Ciao "+current_user.name+" ! "
        return render_template('/Instructor/creaLezioni.html',userName=userName,tableVisible=''' hidden="hidden" ''' ,formVisible='''  ''',corsi=courses,stanze=stanze)  

 
    titleTable = "Slot prenotabili"
    #controllo se la stanza scelta è grande abbastanza per i massimi iscritti alla lezione del corso
    course=session.query(Course).get(corso)
    room=session.query(Room).get(dove)
    dayForPolicy=session.query(Day).filter(Day.date==data).first()
    policy=dayForPolicy.policy_obj
    #se la stanza è piena non torno slot liberi
    if course.maxcostumers>(int(room.max_capacity*(policy.room_percent/100))):
        userName = "Ciao "+current_user.name+" ! "
        slotTuple=tuple()
        flash("Capienza giornaliera stanza inferiore a massime registrazioni alla lezione,cambia stanza o prova un altro giorno")
        return render_template('/Instructor/creaLezioni.html',userName=userName,tableVisible=tableVisible,formVisible=formVisible,titleTable=titleTable,corso=corso,dove=dove,slot=slotTuple)
    else:
        
        #prendo gli slot della giornata,sono costretto a prenderli senza tutti i filtri per come funziona sqlORM
        slots=session.query(Reservation_Slot).filter(Reservation_Slot.day == data).all()
        slotlist=list(slots)
        for slot in slots:
            for lesson in slot.lessons_obj:
                #se il trainer tiene già una lezione in quel corso rimuovo lo slot
                if lesson.course_obj.trainer==current_user.id:
                    slotlist.remove(slot)
                #se c'è una lezione in corso in quella sala rimuovo lo slot
                elif lesson.course_room==dove:
                        slotlist.remove(slot)
        slotTuple=tuple(slotlist)
        #titleTable ="Slot prenotabili per il corso: "+corso+", data: "+data+", dove: "+dove+", slot: "+slot+"."
        # string to show in the navbar of the page
        userName = "Ciao "+current_user.name+" ! "
        return render_template('/Instructor/creaLezioni.html',userName=userName,tableVisible=tableVisible,formVisible=formVisible,titleTable=titleTable,corso=corso,dove=dove,slot=slotTuple)
 


# function to create a lesson for a specified course in a specified slot of time (all specified before)
@instructor.route('/reserveSlot/<int:idSlot>,<int:idCorso>,<int:idRoom>')
@login_required
@at_least_trainer_required
def reserveSlot(idSlot,idCorso,idRoom):
    
    tempLesson=Lesson(idSlot,idCorso,idRoom)
    tempLesson.add_obj()
    return redirect(url_for('instructor.creaLezioni'))


# Function to delete a lesson
@instructor.route('/eliminaLezione/<int:idLezione>')
@login_required
@at_least_trainer_required
def eliminaLezione(idLezione):
    lesson=session.query(Lesson).get(idLezione)
    if(lesson.is_deletable()):
        if( not lesson.delete_obj()):
            flash("impossibile eliminare Lezione")      

    else:
        flash("impossibile eliminare Lezione")    
    return redirect(url_for('instructor.prossimeLezioni'))