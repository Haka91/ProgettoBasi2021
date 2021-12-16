# Blueprint per la sezione user

from flask import Flask
from flask import Blueprint, render_template
from flask.helpers import url_for
from flask_login.utils import login_required
from werkzeug.utils import redirect
from DbController import session
from Models.Users import User,at_least_user_required
from Models.Policies import Policy
from Models.Rooms import Weight_Room,Course_Room,Room
from Models.Reservations import Reservation
from Models.Lessons import Lesson
from Models.Courses import Course



user = Blueprint('user',__name__,url_prefix='/user')

# Route to show the indroduction page.
# It shows the next reservation of the user
@user.route('/introduzione')
@login_required
def introduzione():
    prenotazioni=session.query(Reservation) # CORRECT THE QUERY
    return render_template('/User/introduzione.html', prenotazioni=prenotazioni)


# Active reservations of the user
@user.route('/prenotazioniAttive')
@login_required
def prenotazioniAttive():
    # QUERY NEEDED
    return render_template('/User/prenotazioniAttive.html') 


# Page where is possible to see the bookings for the weight rooms and it is possible to book a reservation for
# one of the weight rooms
@user.route('/prenotaSalaPesi')
@login_required
def prenotaSalaPesi():
    # QUERY NEEDED
    return render_template('/User/prenotaSalaPesi.html') 


# Page where to gerister for a course
@user.route('/iscrizioneAiCorsi')
@login_required
def iscrizioneAiCorsi():
    # REGISTER PERSON TO THE COURSE
    courses=session.query(Course)
    return render_template('/User/iscrizioneAiCorsi.html',courses=courses)


# Page to book lessons
@user.route('/prenotaLezioneCorso')
@login_required
def prenotaLezioneCorso():
    lessons=session.query(Lesson)
    return render_template('/User/prenotaLezioneCorso.html',lessons=lessons) 


# Page to change user's data
@user.route('/cambiaDatiUtente')
@login_required
def cambiaDatiUtente():
    # CHANGE USER DATA
    return render_template('/User/cambiaDatiUtente.html') 


# Function to book weight room on a specific time slot
@user.route('/faiPrenotazioneSalaPesi/<int:id>')
@login_required
def faiPrenotazioneSalaPesi(id):
    # DO STUFF
    return redirect(url_for(user.prenotaSalaPesi))


# Function to book a lesson
@user.route('/faiPrenotazioneLezione/<int:idLesson>')
@login_required
def faiPrenotazioneLezione(idLesson):
    # BOOK LESSON
    return redirect(url_for('user.prenotaLezioneCorso'))
