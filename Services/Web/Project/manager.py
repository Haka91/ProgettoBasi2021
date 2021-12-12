# Blueprint per la sezione user

from flask import Flask,request
from flask import Blueprint, render_template
from flask.helpers import flash
from DbController import session
from Models.Users import User,at_least_manager_required
from Models.Policies import Policy
from Models.Rooms import Weight_Room,Course_Room



manager = Blueprint('manager',__name__,url_prefix='/manager')

# AGGIUNGERE LINK PER OGNI UTENTE PER FARE IN MODO DI MODIFICARE IL SUO STATO DI ATTIVATO O NON ATTIVATO
@at_least_manager_required
@manager.route('/gestioneUtenti')
def gestioneUtenti():
    # mi serve una query:
    users= session.query(User).order_by(User.surname).all()
    # 1) lista di tutti gli utenti ( ruolo , nome, cognome , attivato/nonAttivato )
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
    
    weightRooms=session.query(Weight_Room).all()
    courseRooms=session.query(Course_Room).all()            
    return render_template('/Manager/gestioneSale.html',salePesi=weightRooms,saleCorsi=courseRooms)


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
    return render_template('/Manager/gestioneOrariPalestra.html')

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

# DA FARE:  PAGINA STATISTICHE (?)