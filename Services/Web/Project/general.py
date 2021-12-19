#Questa blueprint sarà per le pagine senza login e per la pagina di login e registrazione


from flask import request
from flask import Blueprint, render_template,flash
from flask.helpers import url_for
from flask_login import current_user,login_user, logout_user
from werkzeug.utils import redirect
from Models.Users import User
from Models.Courses import Course
from Models.Rooms import  Weight_Room, Course_Room

from DbController import session



general = Blueprint('general',__name__)


# homepage

@general.route('/')
def index():
    user=current_user #to see if the user is logged in    
    userName=""
    if current_user.is_anonymous == False:
        userName = "Ciao "+current_user.name+" ! "
    #filtro per i corsi che decido di rendere visibili
    corsi = session.query(Course).filter(Course.isvisible).all()
    salaPesi = session.query(Weight_Room).filter(Weight_Room.isvisible).all()
    salaCorsi = session.query(Course_Room).filter(Course_Room.isvisible).all() 
    return render_template('/General/homepage.html',userName=userName,user=user,corsi=corsi,salaPesi=salaPesi,salaCorsi=salaCorsi) 


# login page
@general.route('/loginPage')
def loginPage():
    return render_template('/General/login.html')


# login function
@general.route('/loginFunzione',methods=['POST'])
def loginFunzione():
    if request.method=='POST':
        login_email=request.form["email"].lower()
        login_password=request.form["password"]  
        user_session=session.query(User).filter_by(email=login_email).first()
        if user_session:
            if user_session.checkpsw(login_password):
                login_user(user_session,True,force=True)
                #we make the session expire after 30 minutes by default
                session.permanent=True               
                
                if user_session.role==1:
                      
                     return redirect(url_for('user.introduzione'))  
                elif user_session.role==2:
                    
                     return redirect(url_for('instructor.introduzione'))   
                elif user_session.role==3:
                      
                     return redirect(url_for('manager.introduzione')) 

               
            else:               
                flash("Credenziali Errate","error")  
                return render_template('/General/login.html')    
        else:           
            flash("Credenziali Errate","error")  
            return render_template('/General/login.html')   
    return


# register page
@general.route('/registerPage' )
def registerPage():
    return render_template('/General/register.html')


# register function
@general.route('/registerFunction',methods=['POST'])
def registerFunction():
    if request.method=='POST':
        
        name=request.form["nome"].lower()
        surname=request.form["cognome"].lower()
        address=request.form["indirizzo"].lower()
        city=request.form["città"].lower()
        email=request.form["email"].lower()
        cellular=request.form["telefono"].lower()
        password=request.form["password"]
        password2=request.form["password2"]
        if(name and surname and address and city and email and cellular and password and password2):
            if(password ==password2):
                temp_user=User(name,surname,email,cellular,address,city,password,1)
                if(temp_user.add_obj()):
                    flash("user registrato")
                    return render_template('/General/login.html')   
                else:
                    flash("user non registrato")
                    return render_template('/General/register.html')
            else:
                flash("le password devono combaciare")
                return render_template('/General/register.html')

        else:
            print("i campi non devono essere vuoti")
            return render_template('/General/register.html')   
       
    return render_template('/General/register.html')


# Logout Function
@general.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('general.index'))