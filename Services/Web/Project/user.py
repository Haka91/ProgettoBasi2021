# Blueprint per la sezione user

from flask import request
from flask import Blueprint, render_template
from flask.helpers import url_for, flash
from flask_login.utils import login_required
from werkzeug.utils import redirect
from DbController import session
from Models.Users import User,at_least_user_required
from Models.Rooms import Weight_Room
from Models.Reservations import Reservation
from Models.Reservation_Slots import Reservation_Slot
from Models.Lessons import Lesson
from Models.Courses import Course
from DbController import session
from flask_login import current_user,logout_user
from datetime import date, datetime, timedelta
from Models.Days import Day
from Models.Reservations import Weight_Room_Reservation
from Models.Reservations import Course_Reservation


user = Blueprint('user',__name__,url_prefix='/user')

# Route to show the indroduction page.
# It shows the next reservation of the user
@user.route('/introduzione')
@login_required
@at_least_user_required
def introduzione():
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    user=session.query(User).get(current_user.id) 
    # query to get the role of the logged user
    #ruolo=session.query(User).get(current_user.role)
    return render_template('/User/introduzione.html',userName=userName, ruolo=user.role, prenotazioni=user.soonReservations())


# Active reservations of the user
@user.route('/prenotazioniAttive')
@login_required
@at_least_user_required
def prenotazioniAttive():
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    
    return render_template('/User/prenotazioniAttive.html',userName=userName,prenotazioni=current_user.fromTodayReservations()) 


# Page where is possible to see the bookings for the weight rooms and it is possible to book a reservation for
# one of the weight rooms
@user.route('/prenotaSalaPesi')
@login_required
@at_least_user_required
def prenotaSalaPesi():
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    #filtro per le stanze visibili
    stanze = session.query(Weight_Room).filter(Weight_Room.isvisible).all()
    tableVisible=''' hidden="hidden" ''' #now the table is NOT visible
    formVisible='''  ''' # now the form is visible
    return render_template('/User/prenotaSalaPesi.html',userName=userName,stanze=stanze,tableVisible=tableVisible,formVisible=formVisible) 


# Function to research available slots on the prenotaSalaPesi page
# It shows the slots available in the selected day and room
@user.route('/filtraSlotSalaPesi', methods = ['POST', 'GET'])
@login_required
@at_least_user_required
def filtraSlotSalaPesi():
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    tableVisible='''  ''' #now the table will be visible
    formVisible=''' hidden="hidden" ''' # now the form is NOT visible
    

    try :
        
        dataString=request.form.get('data')
        roomID = int(request.form["chooseroom"])
        data=datetime.strptime(dataString,'%Y-%m-%d')
        
    except :        
        flash("errore nei campi")


        stanze = session.query(Weight_Room).all()
        tableVisible=''' hidden="hidden" ''' #now the table is NOT visible
        formVisible='''  ''' # now the form is visible
        return render_template('/User/prenotaSalaPesi.html',userName=userName,stanze=stanze,tableVisible=tableVisible,formVisible=formVisible)      

    if(data<=datetime.today() or data>=(datetime.today() +timedelta(days=14) )):
        flash("non puoi cercare prenotazioni antecedenti alla data odierna o successive ai prossimi 14 giorni")
        stanze=session.query(Weight_Room).filter(Weight_Room.isvisible).all()
        tableVisible=''' hidden="hidden" ''' #now the table is NOT visible
        formVisible='''  ''' # now the form is visible
        return render_template('/User/prenotaSalaPesi.html',userName=userName,stanze=stanze,tableVisible=tableVisible,formVisible=formVisible)      

 
    titleTable = "Slot prenotabili"
    #ricavo la policy assieme al  numero massimo di slot e la sala pesi
    
    try:    
        dayWithPolicy=session.query(Day).filter(Day.date==data).first()
        room=session.query(Weight_Room).filter(Weight_Room.id==roomID).first()
        policy=dayWithPolicy.policy_obj 
        prenotationRemaining=policy.max_user_reserv       
    except Exception as e:        
        flash("nessuno slot prenotazione disponibile in questa giornata")
        slots=session.query(Reservation_Slot).filter(Reservation_Slot.day == data).all()
        slotlist=list(slots)
        slotTuple=tuple(slotlist)    
        return render_template('/User/prenotaSalaPesi.html',dataString=dataString,dove=roomID,tableVisible=tableVisible,formVisible=formVisible,weightRoomsSlot=slotTuple)

    #prendo gli slot della giornata
    slots=session.query(Reservation_Slot).filter(Reservation_Slot.day == data).all()
    slotlist=list(slots)
    #controllo aggiuntivo se percaso jinja non ha preso correttamente i campi    
    if(room is not None and dayWithPolicy is not None  and policy is not None):
        prenotationRemaining=policy.max_user_reserv        
        
        for slot in slots:
          
            if  slot.slotFree(int(room.max_capacity*(policy.room_percent/100)),roomID) :
                for weightReservation in slot.weight_reservations_obj:
                    #controllo se ho uno slot qualsiasi già prenotato nella giornata
                   
                    if (weightReservation.user==current_user.id):
                       
                        prenotationRemaining=prenotationRemaining-1
                        slotlist.remove(slot)   
            
        if(len(slotlist)==0):
            flash("nessuno slot prenotazione disponibile in questa giornata")
        if(prenotationRemaining<=0):
            slotlist=list()
            flash("prenotazioni massime raggiunte")
    else:
        flash("seleziona tutti i campi prima di effettuare la ricerca")
    slotTuple=tuple(slotlist)
    
    return render_template('/User/prenotaSalaPesi.html',prenotazioniRimaste=prenotationRemaining,roomID=roomID,userName=userName,dataString=dataString,dove=roomID,tableVisible=tableVisible,formVisible=formVisible,weightRoomsSlot=slotTuple)



# Function to book weight room on a specific time slot
@user.route('/faiPrenotazioneSalaPesi/<int:idRoom>,<int:idSlot>')
@login_required
@at_least_user_required
def faiPrenotazioneSalaPesi(idRoom,idSlot):
     
    slot=session.query(Reservation_Slot).get(idSlot)
    policy=slot.day_obj.policy_obj
    room=session.query(Weight_Room).filter(Weight_Room.id==idRoom).first()
    #ricontrollo che sia ancora libero lo slot   
    if(slot.slotFree(int(room.max_capacity*(policy.room_percent/100)),idRoom)):
       reservation= Weight_Room_Reservation(idRoom,idSlot,current_user.id)       
       if(not reservation.add_obj() ):
          flash("impossibile inserire prenotazione")
    else:
         flash("slot orario pieno")    
    return redirect(url_for('user.prenotaSalaPesi'))



# Page where to gerister for a course
@user.route('/iscrizioneAiCorsi')
@login_required
@at_least_user_required
def iscrizioneAiCorsi():
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    #filtro per i corsi visibili
    courses=session.query(Course).filter(Course.isvisible).all()
    tableVisible=''' hidden="hidden" ''' #now the table will be hidden
    formVisible='''  ''' # now the form is visible
    return render_template('/User/iscrizioneAiCorsi.html',userName=userName,courses=courses,tableVisible=tableVisible,formVisible=formVisible)


# Page to change user's data
@user.route('/cambiaDatiUtente')
@login_required
@at_least_user_required
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
@at_least_user_required
def modificaDatiUtente():
    
    try:
        name = request.form.get('nome')    
        surname = request.form.get('cognome')        
        cellular = request.form.get('telefono')
        address = request.form.get('indirizzo')
        city = request.form.get('citta')
        usertoChange=session.query(User).get(current_user.id)
        if(usertoChange.update_obj(name,surname,cellular,address,city)):
            flash("modifica dati utente avvenuta con successo!")
    except:
        flash("errore nei campi")
        return redirect(url_for('user.cambiaDatiUtente'))

    
    return redirect(url_for('user.cambiaDatiUtente'))


# Function to modify user password
@user.route('/modificaPasswordUtente', methods = ['POST', 'GET'])
@login_required
@at_least_user_required
def modificaPasswordUtente():
    oldPassword = ""
    newPassword = ""
    newPassword2 = ""

    try:
        oldPassword = request.form['password']
        newPassword = request.form['newPassword']
        newPassword2 = request.form['newPassword2']
        if(newPassword == newPassword2):
            if  ( not current_user.update_password(oldPassword,newPassword)) :
                  flash('Errore nel cambio password')
            else:
                    logout_user()
                    flash('Modifica password avvenuta con successo')
                    return redirect(url_for('general.index'))

               
        else:
            flash('Nuova password e conferma nuova password diverse')
    except:
        flash('Errore nel cambio password controlla i campi')

    
    return redirect(url_for('user.cambiaDatiUtente'))


# Function that filters the lessons based on the selection of a course on the iscrizioneAiCorsi.html page
@user.route('/filtraLezioniCorsi', methods = ['POST', 'GET'])
@login_required
@at_least_user_required
def filtraLezioniCorsi():
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    tableVisible='''  ''' #now the table will be visible
    formVisible=''' hidden="hidden" ''' # now the form is NOT visible
    lessons=list()
    try:
        idCorso = request.form.get('corsi')
        corso = session.query(Course).get(idCorso)
        lessonsTuple=corso.lessons_obj
        
        for lesson in lessonsTuple:
            
            if lesson.lessonSlotFree():                         
                #controllo che la prenotazione non sia più vecchia di oggi e che l'user non ne abbia già fatta una nello stesso slot
                alreadyRegistered=False
                
                if lesson.reservation_slot_obj.day>date.today(): 
                    for courseReservation in  lesson.course_reservations_obj:
                        
                        if(courseReservation.user == current_user.id):
                               alreadyRegistered=True
                              
                    if not alreadyRegistered:
                            lessons.append(lesson)
                
            
            
       
    except Exception as e:
       print(e)
       flash("impossibile recuperare lista Lezioni")  
       redirect(url_for('user.iscrizioneAiCorsi'))
    lessonResult=tuple(lessons)
    return render_template('/User/iscrizioneAiCorsi.html',tableVisible=tableVisible,formVisible=formVisible,userName=userName,lessons=lessonResult)


# Function to book a lesson
@user.route('/faiPrenotazioneLezione/<int:idLezione>')
@login_required
@at_least_user_required
def faiPrenotazioneLezione(idLezione):
    lesson=session.query(Lesson).get(idLezione)
    if(lesson.lessonSlotFree()):
        courseReservation=Course_Reservation(idLezione,current_user.id)
        if not courseReservation.add_obj():
            flash("impossibile iscriversi alla lezione")
        else :flash("prenotazione effettuata con successo")
    else:
        flash("impossibile iscriversi alla lezione")
    return redirect(url_for('user.iscrizioneAiCorsi'))


# Function to delete a booking
@user.route('/eliminaPrenotazione/<int:idPrenotazione>')
@login_required
@at_least_user_required
def eliminaPrenotazione(idPrenotazione):
    reservation=session.query(Reservation).get(idPrenotazione)
    if(not reservation.delete_obj()):
        flash("prenotazione cancellata")
    return redirect(url_for('user.prenotazioniAttive'))
