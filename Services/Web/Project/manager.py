# Blueprint per la sezione user

from flask import Flask,request
from flask import Blueprint, render_template
from flask_login.utils import login_required
from flask.helpers import flash, url_for
from sqlalchemy.sql.sqltypes import ARRAY
from werkzeug.utils import redirect
from DbController import session
from Models.Users import User,at_least_manager_required
from Models.Policies import Policy
from Models.Rooms import Weight_Room,Course_Room,Room
from Models.Courses import Course
from Models.Days import Day
from flask_login import current_user





manager = Blueprint('manager',__name__,url_prefix='/manager')

# Introduction page
@manager.route('/introduzione')
@login_required
@at_least_manager_required
def introduzione():
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    numTrainers=session.query(User).filter(User.role==2).count()
    numUsers=session.query(User).filter(User.role==3).count()
    return render_template('/Manager/introduzione.html',userName=userName,numTrainers=numTrainers,numUsers=numUsers)


@manager.route('/gestioneUtenti')
@login_required
@at_least_manager_required
def gestioneUtenti():
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    users= session.query(User).order_by(User.surname).filter(User.role==1).all()
    return render_template('/Manager/gestioneUtenti.html',userName=userName,utenti=users)


@manager.route('/gestioneSale',methods=['POST','GET'])
@login_required
@at_least_manager_required
def gestioneSale(): 
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "

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
    return render_template('/Manager/gestioneSale.html',userName=userName,weightRooms=weightRooms,courseRooms=courseRooms)


@manager.route('/gestioneTrainers')
@login_required
@at_least_manager_required
def gestioneTrainers():
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    trainers= session.query(User).order_by(User.surname).filter(User.role==2).all()
    users= session.query(User).order_by(User.surname).filter(User.role==1).all()
    return render_template('/Manager/gestioneTrainers.html',userName=userName,trainers=trainers,users=users) # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE


@manager.route('/gestioneOrariPalestra',methods=['POST','GET'])
@login_required
@at_least_manager_required
def gestioneOrariPalestra():
    from Models.Days import Day
    from datetime import date, datetime, time, timedelta
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    if request.method=='POST':
        policy=request.form.get("policy")
        try :
            startingDateString=request.form.get('dataInizio')
            startingDate=datetime.strptime(startingDateString,'%Y-%m-%d')
            endingDateString=request.form.get('dataFine')
            endingDate=datetime.strptime(endingDateString,'%Y-%m-%d')
            
        except:
            flash("selezionare una data")
            days=session.query(Day).order_by(Day.date).all()    
            policies=session.query(Policy).all()
            return render_template('/Manager/gestioneOrariPalestra.html',userName=userName,policies=policies,days=days)
        if(startingDate<datetime.today()):
            days=session.query(Day).order_by(Day.date).all()    
            policies=session.query(Policy).all()
            flash("non puoi creare giorni posteriori ad oggi")
            return render_template('/Manager/gestioneOrariPalestra.html',userName=userName,policies=policies,days=days)
        try :
            openingTimeH=int(request.form['ora_apertura'])
            openingTimeM=int(request.form['minuto_apertura'])
            breakTimeH=int(request.form['ora_inizioPausaPranzo'])
            breakTimeM=int(request.form['minuto_inizioPausaPranzo'])
            breakTimeDuration=int(request.form.get('durataPausaPranzo'))
            closingTimeH=int(request.form['ora_chiusura'])
            closingTimeM=int(request.form['minuto_chiusura']) 
        except:
            flash("errore nei campi")
            days=session.query(Day).order_by(Day.date).all()    
            policies=session.query(Policy).all()
            return render_template('/Manager/gestioneOrariPalestra.html',userName=userName,policies=policies,days=days)

        while startingDate <=endingDate:
            if(breakTimeDuration>0 and breakTimeH and breakTimeM):
                day=Day(startingDate,datetime(startingDate.year,startingDate.month,startingDate.day,openingTimeH,openingTimeM),datetime(startingDate.year,startingDate.month,startingDate.day,closingTimeH,closingTimeM),policy=policy,break_slot=breakTimeDuration,break_time=datetime(startingDate.year,startingDate.month,startingDate.day,breakTimeH,breakTimeM))     
            else:    
                day=Day(startingDate,datetime(startingDate.year,startingDate.month,startingDate.day,openingTimeH,openingTimeM),datetime(startingDate.year,startingDate.month,startingDate.day,closingTimeH,closingTimeM),policy=policy,break_slot=0) 
            
            day.add_obj()                
           
               

            startingDate=startingDate + timedelta(days=1) 

    days=session.query(Day).order_by(Day.date).all()    
    policies=session.query(Policy).all()
    return render_template('/Manager/gestioneOrariPalestra.html',userName=userName,policies=policies,days=days)


@manager.route('/gestionePolicy',methods=['POST','GET'])
@login_required
@at_least_manager_required
def gestionePolicy(): 
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    
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
                
    return render_template('/Manager/gestionePolicy.html',userName=userName,policies=policies)


# Function for changing the state of a user (activated <-> deactivate)
@manager.route('/attivaDisattivaUser/<int:idUser>')
@login_required
@at_least_manager_required
def attivaDisattivaUser(idUser):
    utente = session.query(User).get(idUser)
    utente.activate_or_deactivate_obj()
    print(utente.name, utente.is_active)
    return redirect(url_for('manager.gestioneUtenti'))


# Function to change role of  User in Trainer
@manager.route('/userToTrainer/<int:idUser>')
@login_required
@at_least_manager_required
def userToTrainer(idUser):
    user=session.query(User).get(idUser)
    if(not user.update_role(2)):
        flash("impossibile cambiare ruolo all'utente selezionato")
    return redirect(url_for('manager.gestioneTrainers'))


# Function to change role of a Trainer to User
@manager.route('/trainerToUser/<int:idUser>')
@login_required
@at_least_manager_required
def trainerToUser(idUser):
    user=session.query(User).get(idUser)
    if(not user.update_role(1)):
        flash("impossibile cambiare ruolo all'utente selezionato")
    return redirect(url_for('manager.gestioneTrainers'))


# Function to delete a room
@manager.route('/eliminaSala/<int:idSala>')
@login_required
@at_least_manager_required
def eliminaSala(idSala):
    room=session.query(Room).get(idSala)
    #dato che è uso la joinetable inheritance su Rooms devo controllare cosa sono
    if(room.is_weight):
        weightRoom=session.query(Weight_Room).get(idSala)
        if  weightRoom.is_deletable():
            weightRoom.delete_obj()
    else:
        courseRoom=session.query(Course_Room).get(idSala)
        if courseRoom.is_deletable():
            courseRoom.delete_obj()

    return redirect(url_for('manager.gestioneSale'))


# Function to delete a date
@manager.route('/eliminaData/<int:data>')
@login_required
@at_least_manager_required
def eliminaData(data):
    # DO STUFF
    return redirect(url_for('manager.gestioneOrariPalestra'))


# Function do delete a Policy
@manager.route('/eliminaPolicy/<int:idPolicy>')
@login_required
@at_least_manager_required
def eliminaPolicy(idPolicy):
    policy=session.query(Policy).get(idPolicy)    
    if( policy.is_deletable()):
        policy.delete_obj()
    
    return redirect(url_for('manager.gestionePolicy'))


# Function to delete a course
@manager.route('/eliminaCorso/<int:idCorso>')
@login_required
@at_least_manager_required
def eliminaCorso(idCorso):
    course=session.query(Course).get(idCorso)
    if(course.isDeletable()):
        course.delete_obj()
    return redirect(url_for('manager.gestioneCorsi'))


# Page for managing the courses offered
@manager.route('/gestioneCorsi')
@login_required
@at_least_manager_required
def gestioneCorsi():
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "
    courses=session.query(Course).all()   
    trainers= session.query(User).order_by(User.surname).filter(User.role==2).all()
    return render_template('Manager/gestioneCorsi.html',userName=userName,corsi=courses,trainers=trainers)


# Function to visualize the statistics of a specified trainer
@manager.route('/infoTrainer/<int:idUser>')
def infoTrainer(idUser):
    # string to show in the navbar of the page
    userName = "Ciao "+current_user.name+" ! "    
    
    trainerObj=session.query(User).get(idUser)

    numeroCorsiInsegnati = len(trainerObj.courses_obj)
    numeroLezioni = 0
    for course in trainerObj.courses_obj:
        numeroLezioni=numeroLezioni + len(course.lessons_obj)
    return render_template('Manager/infoTrainer.html',userName=userName,numeroLezioni=numeroLezioni,numeroCorsiInsegnati=numeroCorsiInsegnati)


# Function that creates a course
@manager.route('/creaCorso', methods=['POST'])
@login_required
@at_least_manager_required
def creaCorso():
    if request.method=='POST':
        try:
            name=request.form["nome"].lower()
            description=request.form["descrizione"].lower()
            trainer=int(request.form.get("selectTrainer"))
            maxcostumers=int(request.form.get("maxcostumers"))
        except:  
            flash("Errore nei campi","error") 
            courses=session.query(Course).all() 
            return redirect(url_for('manager.gestioneCorsi',corsi=courses))
      
        if(name and description and trainer and maxcostumers):
            courseToAdd=Course(name,description,trainer ,maxcostumers)
            if not (courseToAdd.add_obj()): 
                flash("Impossibile aggiungere corso")

          
        else:
                flash("Errore nei campi","error")
    courses=session.query(Course).all()   
                
    
    return redirect(url_for('manager.gestioneCorsi',corsi=courses))


# Function to activate / deactivate a specifico course
@manager.route('attivaDisattivaCorso/<int:idCorso>')
@login_required
@at_least_manager_required
def attivaDisattivaCorso(idCorso):
    corso = session.query(Course).get(idCorso)
    corso.activate_or_deactivate_obj()
    return redirect(url_for('manager.gestioneCorsi'))


# Function to delete a selected time table for a specified range of days
@manager.route('/eliminazioneOrariPalestra/<int:idDay>')
@login_required
@at_least_manager_required
def eliminazioneOrariPalestra(idDay):
    dayToDelete=session.query(Day).get(idDay)
    if(dayToDelete.is_deletable()):
        dayToDelete.delete_obj()
    else:
        flash("Impossibile elimare il giorno")
    return redirect(url_for('manager.gestioneOrariPalestra'))