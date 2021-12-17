# Blueprint per la sezione user

from flask import Flask, request
from flask import Blueprint, render_template
from flask.helpers import url_for, flash
from flask_login.utils import login_required
from werkzeug.utils import redirect
from DbController import session
from Models.Users import User,at_least_user_required
from Models.Policies import Policy
from Models.Rooms import Weight_Room,Course_Room,Room
from Models.Reservations import Reservation
from Models.Reservation_Slots import Reservation_Slot
from Models.Lessons import Lesson
from Models.Courses import Course
from DbController import session
from flask_login import current_user
from datetime import datetime, timedelta
from Models.Days import Day


user = Blueprint('user',__name__,url_prefix='/user')

# Route to show the indroduction page.
# It shows the next reservation of the user
@user.route('/introduzione')
@login_required
def introduzione():
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    prenotazioni=session.query(Reservation) # CORRECT THE QUERY
    return render_template('/User/introduzione.html',userName=userName, prenotazioni=prenotazioni)


# Active reservations of the user
@user.route('/prenotazioniAttive')
@login_required
def prenotazioniAttive():
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    # QUERY NEEDED
    return render_template('/User/prenotazioniAttive.html',userName=userName) 


# Page where is possible to see the bookings for the weight rooms and it is possible to book a reservation for
# one of the weight rooms
@user.route('/prenotaSalaPesi')
@login_required
def prenotaSalaPesi():
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    stanze = session.query(Weight_Room).all()
    tableVisible=''' hidden="hidden" ''' #now the table is NOT visible
    formVisible='''  ''' # now the form is visible
    return render_template('/User/prenotaSalaPesi.html',userName=userName,stanze=stanze,tableVisible=tableVisible,formVisible=formVisible) 


# Function to research available slots on the prenotaSalaPesi page
# It shows the slots available in the selected day and room
@user.route('/filtraSlotSalaPesi', methods = ['POST', 'GET'])
@login_required
def filtraSlotSalaPesi():
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    tableVisible='''  ''' #now the table will be visible
    formVisible=''' hidden="hidden" ''' # now the form is NOT visible

    try :
        
        dataString=request.form.get('data')
        roomID = int(request.form["chooseroom"])      
        print(dataString)
        data=datetime.strptime(dataString,'%Y-%m-%d')
        
    except :        
        flash("errore nei campi")


        stanze = session.query(Weight_Room).all()
        tableVisible=''' hidden="hidden" ''' #now the table is NOT visible
        formVisible='''  ''' # now the form is visible
        return render_template('/User/prenotaSalaPesi.html',userName=userName,stanze=stanze,tableVisible=tableVisible,formVisible=formVisible)      

    if(data<=datetime.today() or data>=(datetime.today() +timedelta(days=14) )):
        flash("non puoi cercare prenotazioni antecedenti alla data odierna o successive ai prossimi 14 giorni")
        stanze=session.query(Course_Room).all()
        tableVisible=''' hidden="hidden" ''' #now the table is NOT visible
        formVisible='''  ''' # now the form is visible
        return render_template('/User/prenotaSalaPesi.html',userName=userName,stanze=stanze,tableVisible=tableVisible,formVisible=formVisible)      

 
    titleTable = "Slot prenotabili"
    #ricavo la policy con il numero massimo di slot e la sala pesi
    print(roomID)
    try:    
        dayWithPolicy=session.query(Day).filter(Day.date==data).first()
        room=session.query(Weight_Room).filter(Weight_Room.id==roomID).first()
        policy=dayWithPolicy.policy_obj
        print(policy.name,policy.room_percent,policy.max_user_reserv)
    except Exception as e:        
        flash("nessuno slot prenotazione disponibile in questa giornata")
        slots=session.query(Reservation_Slot).filter(Reservation_Slot.day == data).all()
        slotlist=list(slots)
        slotTuple=tuple(slotlist)    
        return render_template('/User/prenotaSalaPesi.html',dataString=dataString,dove=roomID,tableVisible=tableVisible,formVisible=formVisible,weightRoomsSlot=slotTuple)

    #prendo gli slot della giornata,sono costretto a prenderli senza tutti i filtri per come funziona sqlORM
    slots=session.query(Reservation_Slot).filter(Reservation_Slot.day == data).all()
    slotlist=list(slots)
    #controllo aggiuntivo se percaso jinja non ha preso correttamente i campi
    if(room and dayWithPolicy and policy):
        prenotationRemaining=policy.max_user_reserv
        for slot in slots:
            if not slot.slotFull(int(room.max_capacity*(policy.room_percent/100)),roomID) :
                for weightReservation in slot.weight_reservations_obj:
                    #controllo se ho uno slot qualsiasi già prenotato nella giornata
                    if (weightReservation.user==current_user.id):
                        prenotationRemaining=prenotationRemaining-1
                        slotlist.remove(slot)
                    
                else:
                    slotlist.remove(slot)
        if(len(slotlist)==0):
            flash("nessuno slot prenotazione disponibile in questa giornata")
    else:
        flash("seleziona tutti i campi prima di effettuare la ricerca")
    slotTuple=tuple(slotlist)
    # weightRooms = QUERY FOR SLOTS NEEDED
    return render_template('/User/prenotaSalaPesi.html',roomID=roomID,userName=userName,dataString=dataString,dove=roomID,tableVisible=tableVisible,formVisible=formVisible,weightRoomsSlot=slotTuple)



# Function to book weight room on a specific time slot
@user.route('/faiPrenotazioneSalaPesi/<int:idRoom>,<int:idSlot>')
@login_required
def faiPrenotazioneSalaPesi(idRoom,idSlot):
    # BOOK SLOT
    return redirect(url_for('user.prenotaSalaPesi'))



# Page where to gerister for a course
@user.route('/iscrizioneAiCorsi')
@login_required
def iscrizioneAiCorsi():
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    # REGISTER PERSON TO THE COURSE
    courses=session.query(Course)
    return render_template('/User/iscrizioneAiCorsi.html',userName=userName,courses=courses)


# Page to change user's data
@user.route('/cambiaDatiUtente')
@login_required
def cambiaDatiUtente():
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    # retireve the current user
    nome = current_user.name
    cognome = current_user.surname
    email = current_user.email
    telefono = current_user.cellular
    indirizzo = current_user.address
    citta = current_user.city
    return render_template('/User/cambiaDatiUtente.html',userName=userName,nome = nome,cognome=cognome,email=email,telefono=telefono,indirizzo=indirizzo,citta=citta)


@user.route('/modificaDatiUtente', methods = ['POST', 'GET']) 
@login_required
def modificaDatiUtente():
    
    try:
        current_user.name = request.form.get('nome')    
        current_user.surname = request.form.get('cognome')
        current_user.email = request.form.get('email')
        current_user.cellular = request.form.get('telefono')
        current_user.address = request.form.get('indirizzo')
        current_user.city = request.form.get('citta')
    
    except:
        flash("errore nei campi")
        return redirect(url_for('user.cambiaDatiUtente'))

    flash("modifica dati utente avvenuta con successo!")
    return redirect(url_for('user.cambiaDatiUtente'))


# Function to modify user password
@user.route('/modificaPasswordUtente', methods = ['POST', 'GET'])
@login_required
def modificaPasswordUtente():
    oldPassword = ""
    newPassword = ""
    newPassword2 = ""

    try:
        oldPassword = request.form.get('password')
        newPassword = request.form.get('newPassword')
        newPassword2 = request.form.get('newPassword2')
        if(newPassword == newPassword2):
            if  (current_user.update_password(oldPassword,newPassword)) :
                current_user.password = newPassword
            else:
                #non torniamo troppe informazioni,potremmo renderci vulnerabili ad attacchi
                flash('Errore nel cambio password')
        else:
            flash('Nuova password e conferma nuova password diverse')
    except:
        flash('Errore nel cambio password controlla i campi')

    flash('Password cambiata correttamente')
    return redirect(url_for('user.cambiaDatiUtente'))


# Function to book a lesson
@user.route('/faiPrenotazioneLezione/<int:idLesson>')
@login_required
def faiPrenotazioneLezione(idLesson):
    # BOOK LESSON
    return redirect(url_for('user.prenotaLezioneCorso'))


# Page to see the name, trainer name and description of a specific course
@user.route('/infoCorso/<int:idCorso>,<string:nomeCorso>,<string:nomeTrainer>,<string:descrizione>')
@login_required
def infoCorso(idCorso,nomeCorso,nomeTrainer,descrizione):
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    return render_template('/User/infoCorso.html',userName=userName,nomeCorso=nomeCorso,nomeTrainer=nomeTrainer,descrizione=descrizione)