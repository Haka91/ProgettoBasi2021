#Questa blueprint sarà per le pagine senza login e per la pagina di login e registrazione

from flask import Flask,request
from flask import Blueprint, render_template,flash
from flask.helpers import url_for
from flask_login import current_user,login_user, logout_user,login_manager
from sqlalchemy.sql.expression import true
from werkzeug.utils import redirect
from Models.Users import User
from Models.Courses import Course
from Models.Rooms import Room, Weight_Room, Course_Room

from DbController import session



general = Blueprint('general',__name__)


# homepage

@general.route('/')
def index():
    user=current_user #to see if the user is logged in    
    corsi = session.query(Course).all()
    salaPesi = session.query(Weight_Room).all()
    salaCorsi = session.query(Course_Room).all() 
    return render_template('/General/homepage.html',user=user,corsi=corsi,salaPesi=salaPesi,salaCorsi=salaCorsi) # UNA VOLTA PRESENTI LE QUERY PASSARE I DATI AL TEMPLATE


# login page
@general.route('/loginPage')
def loginPage():
    return render_template('/General/login.html')


# login function
@general.route('/loginFunzione',methods=['POST'])
def loginFunzione():
    if request.method=='POST':
        login_email=request.form["email"]
        login_password=request.form["password"]  
        user_session=session.query(User).filter_by(email=login_email).first()
        if user_session:
            if user_session.checkpsw(login_password):
                login_user(user_session,true,force=true)               
                #flash("login avvenuto con successo","Success")
                if user_session.role==1:
                     #return render_template('/User/introduzione.html')  
                     return redirect(url_for('user.introduzione'))  
                elif user_session.role==2:
                     #return render_template('/Instructor/introduzione.html') 
                     return redirect(url_for('instructor.introduzione'))   
                elif user_session.role==3:
                     #return render_template('/Manager/introduzione.html')   
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
        password=request.form["password"].lower()
        password2=request.form["password2"].lower()
        if(name and surname and address and city and email and cellular and password and password2):
            # INSERT CHECK OF PASSWORD AND PASSWORD2
            temp_user=User(name,surname,email,cellular,address,city,password,1)
            if(temp_user.add_obj()):
                print("user registrato")
                return render_template('/General/login.html')   
            else:
                print("user non registrato")
                return render_template('/General/register.html')   
        else:
            print("campi vuoti")
            return render_template('/General/register.html')   
       
    return render_template('/General/register.html')


# Logout Function
@general.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('general.index'))