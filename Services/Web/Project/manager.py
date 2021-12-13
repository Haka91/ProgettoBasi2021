# Blueprint per la sezione user

from flask import Flask,request
from flask import Blueprint, render_template
from flask.helpers import flash, url_for
from sqlalchemy.sql.sqltypes import ARRAY
from werkzeug.utils import redirect
from DbController import session
from Models.Users import User,at_least_manager_required
from Models.Policies import Policy
from Models.Rooms import Weight_Room,Course_Room,Room
from Models.Courses import Course




manager = Blueprint('manager',__name__,url_prefix='/manager')

@at_least_manager_required
@manager.route('/introduzione')
def introduzione():
    numTrainers=session.query(User).filter(User.role==2).count()
    numUsers=session.query(User).filter(User.role==3).count()
    return render_template('/Manager/introduzione.html',numTrainers=numTrainers,numUsers=numUsers)

# AGGIUNGERE LINK PER OGNI UTENTE PER FARE IN MODO DI MODIFICARE IL SUO STATO DI ATTIVATO O NON ATTIVATO
@at_least_manager_required
@manager.route('/gestioneUtenti')
def gestioneUtenti():
    users= session.query(User).order_by(User.surname).filter(User.role==1).all()
    return render_template('/Manager/gestioneUtenti.html',utenti=users) # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE

@at_least_manager_required
@manager.route('/gestioneSale',methods=['POST','GET'])
def gestioneSale(): 

    if request.method=='POST':
        name=request.form["nome"].lower()
        description=request.form["descrizione"].lower()
        roomCapacity=request.form["capienza"].lower()
        isWeight=request.form.get("isWeight")
        if(name and roomCapacity and description):
            if(isWeight):
                tempRoom=Weight_Room(name,description,roomCapacity)
            else:
                tempRoom=Course_Room(name,description,roomCapacity)
            
            if not (tempRoom.add_obj()): 
                flash("Impossibile aggiungere Stanza")

    
        else:
                flash("Errore nei campi","error")
    
    #weightRooms=session.query(Weight_Room).all()
    #courseRooms=session.query(Course_Room).all()      
    rooms=session.query(Room).all()      
    #return render_template('/Manager/gestioneSale.html',salePesi=weightRooms,saleCorsi=courseRooms)
    return render_template('/Manager/gestioneSale.html',rooms=rooms)


@at_least_manager_required
@manager.route('/gestioneTrainers')
def gestioneTrainers():

    trainers= session.query(User).order_by(User.surname).filter(User.role==2).all()
    # 1) lista di tutti gli utenti ( ruolo , nome, cognome , attivato/nonAttivato )    
   
    # mi serve una query:
    # 1) lista di tutti i trainers ( nome , cognome , attivatoNonAttivato , allenaCorsi? (true oppure false) )
    # 2) lista di tutti gli utenti che non sono trainers oppure che non è il gestore ( nome, cognome , attivato/nonAttivato )
    users= session.query(User).order_by(User.surname).filter(User.role==1).all()
    return render_template('/Manager/gestioneTrainers.html',trainers=trainers,users=users) # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE

@at_least_manager_required
@manager.route('/gestioneOrariPalestra')
def gestioneOrariPalestra():
    # mi serve una query:
    # 1) 7 stringhe, ogni stringa rappresentante gli orari di apertura e chiusura della palestra
    policies=session.query(Policy).all()
    return render_template('/Manager/gestioneOrariPalestra.html',policies=policies)

@at_least_manager_required
@manager.route('/gestionePolicy',methods=['POST','GET'])
def gestionePolicy(): 
    
    if request.method=='POST':
        name=request.form["name"].lower()
        room_percent=request.form["occupazione"].lower()
        max_users=request.form["maxriservazioni"].lower()
        if(name and room_percent and max_users):
            policyToAdd=Policy(name,room_percent,max_users)
            if not (policyToAdd.add_obj()): 
                flash("Impossibile aggiungere policy")

          
        else:
                flash("Errore nei campi","error")
    policies= session.query(Policy).all()
                
    return render_template('/Manager/gestionePolicy.html',policies=policies)

# Function for changing the state of a user (activated <-> deactivate)
@at_least_manager_required
@manager.route('/attivaDisattivaUser/<int:idUser>')
def attivaDisattivaUser(idUser):
    # DO STUFF
    return redirect(url_for(manager.gestioneUtenti))

# Function to trasform User in Trainer
@at_least_manager_required
@manager.route('/userToTrainer/<int:idUser>')
def userToTrainer(idUser):
    # DO STUFF
    return redirect(url_for(manager.gestioneTrainer))

# Function to delete a Trainer
@at_least_manager_required
@manager.route('/eliminaTrainer/<int:idUser>')
def eliminaTrainer(idUser):
    # DO STUFF
    return redirect(url_for(manager.gestioneTrainer))

# Function to delete a room
@at_least_manager_required
@manager.route('/eliminaSala/<int:idSala>')
def eliminaSala(idSala):
    # DO STUFF
    return redirect(url_for(manager.gestioneSale))

# Function to delete a date
@at_least_manager_required
@manager.route('/eliminaData/<int:data>')
def eliminaData(data):
    # DO STUFF
    return redirect(url_for(manager.gestioneOrariPalestra))

# Function do delete a Policy
@at_least_manager_required
@manager.route('/eliminaPolicy/<int:idPolicy>')
def eliminaPolicy(idPolicy):
    # DO STUFF
    return redirect(url_for(manager.gestionePolicy))

# Function to create a new Room
<<<<<<< HEAD

@manager.route('/eliminaCorso/<int:idCorso>')
@login_required
@at_least_manager_required
def eliminaCorso(idCorso):
=======
@at_least_manager_required
@manager.route('/eliminaStanza/<int:idStanza>')
def eliminaStanza(idStanza):
>>>>>>> 8a7a9e9461222dd7162301ab09d2dda45ac6dfd6
    # DO STUFF
    return redirect(url_for(manager.gestioneCorsi))

# Loads the page for the management of the courses
@at_least_manager_required
@manager.route('/gestioneCorsi')
def gestioneCorsi():
<<<<<<< HEAD
    courses=session.query(Course).all()
    stanze=session.query(Room).all()
    istruttori=session.query(User).order_by(User.surname).filter(User.role==2).all()
=======
    return render_template('Manager/gestioneCorsi.html')
>>>>>>> 8a7a9e9461222dd7162301ab09d2dda45ac6dfd6
