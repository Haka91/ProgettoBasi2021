# Blueprint per la sezione user

from flask import Flask
from flask import Blueprint, render_template, redirect, url_for
from flask_login.utils import login_required
from flask.helpers import url_for
from DbController import session
from flask_login import current_user
from Models.Courses import Course
from Models.Lessons import Lesson
from Models.Rooms import Room
from Models.Users import User,at_least_trainer_required





instructor = Blueprint('instructor',__name__,url_prefix='/instructor')

# Introduction page

@instructor.route('/introduzione')
@login_required
@at_least_trainer_required
def introduzione():
    corsi=session.query(Course).filter_by(trainer=current_user.id).all() #FILTRARE SOLO PER I CORSI FATTI DALL'ISTRUTTORE 
    lezioni=session.query(Lesson).all() #FILTRARE SOLO PER LE LEZIONI DEI CORSI CHE FA L'ISTRUTTORE NELLA PROSSIMA SETTIMANA (O NEI PROSSIMI GIORNI) 
    return render_template('/Instructor/introduzione.html',lezioni=lezioni,corsi=corsi) 

# Page where the next lessons are listed

@instructor.route('/prossimeLezioni')
@login_required
@at_least_trainer_required
def prossimeLezioni():
    lezioni=session.query(Lesson).all() #FILTRARE SOLO PER LE LEZIONI CHE L'ISTRUTTORE FARA' DA OGGI IN POI
    return render_template('/Instructor/prossimeLezioni.html',lezioni=lezioni) 


@instructor.route('/creaLezioni')
@login_required
@at_least_trainer_required
def creaLezioni():
    corsi=session.query(Course).all() #FILTRARE SOLO I CORSI INSEGNATI DALL'ISTRUTTORE
    rooms=session.query(Room).all() 
    return render_template('/Instructor/creaLezioni.html',corsi=corsi,rooms=rooms)

# METODO PER INSERIRE LE LEZIONI NEL DB, IL METODO VA POI AGGIUNTO NEL FORM CHE SI TROVA NELL'HTML (PRE SPECIFICARE L'AZIONE DEL FORM) - FATTO

@instructor.route('/inserisciLezioni', methods = ['POST', 'GET'])
@login_required
@at_least_trainer_required
def inserisciLezioni():
    # INSERIRE LE LEZIONI NEL DB
    return redirect(url_for(instructor.prossimeLezioni))  # ridirezione l'istruttore, dopo l'inserimento delle lezioni, verso la lista delle sue lezioni da fare
