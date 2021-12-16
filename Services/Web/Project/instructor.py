# Blueprint per la sezione user

from flask import Flask, request
from flask import Blueprint, render_template, redirect, url_for
from flask_login.utils import login_required
from flask.helpers import url_for
from DbController import session
from flask_login import current_user
from Models.Courses import Course
from Models.Lessons import Lesson
from Models.Rooms import Room, Course_Room
from Models.Users import User,at_least_trainer_required




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
    lezioni=session.query(Lesson).all() #FILTRARE SOLO PER LE LEZIONI CHE L'ISTRUTTORE FARA' DA OGGI IN POI
    return render_template('/Instructor/prossimeLezioni.html',lezioni=lezioni) 


# Page to create new lessons of an existing course
@instructor.route('/creaLezioni')
@login_required
@at_least_trainer_required
def creaLezioni():
    tableVisible=''' hidden="hidden" ''' #now the table is NOT visible
    formVisible='''  ''' # now the form is visible
    corsi=session.query(Course).all()
    stanze=session.query(Course_Room).all()
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
    #titleTable ="Slot prenotabili per il corso: "+corso+", data: "+data+", dove: "+dove+", slot: "+slot+"."
    return render_template('/Instructor/creaLezioni.html',tableVisible=tableVisible,formVisible=formVisible,titleTable=titleTable,corso=corso,dove=dove)


# function to create a lesson for a specified course in a specified slot of time (all specified before)
@instructor.route('/reserveSlot/<int:idSlot>,<int:idCorso>,<int:idRoom>')
@login_required
@at_least_trainer_required
def reserveSlot(idSlot,idCorso,idRoom):
    # RESERVE SLOT
    #print(idSlot+", "+idCorso+", "+idRoom+". ")
    return redirect(url_for('instructor.creaLezioni'))