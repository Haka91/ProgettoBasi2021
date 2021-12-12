#Questa blueprint sarà per le pagine senza login e per la pagina di login e registrazione

from flask import Flask,request
from flask import Blueprint, render_template,flash
from flask_login import current_user,login_user, logout_user,login_manager
from sqlalchemy.sql.expression import true
from Models.Users import User
from Models.Courses import Course

from DbController import session



general = Blueprint('general',__name__)


# homepage

@general.route('/')
def index():
    # mi servono due query:
    # 1) lista dei corsi (nome corso, nome istruttore, data inizio, data fine)  
    # 2) lista delle sale (nome sala, capienza)  
    # ---
    # Secondo te inseriamo pure gli orari di apertura e chiusura?
    courses = session.query(Course).all()
     
    
    return render_template('/General/homepage.html',corsi=courses) # UNA VOLTA PRESENTI LE QUERY PASSARE I DATI AL TEMPLATE


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
                     return render_template('/User/introduzione.html')    
                elif user_session.role==2:
                     return render_template('/Instructor/introduzione.html')    
                elif user_session.role==3:
                     return render_template('/Manager/gestioneOrariPalestra.html')    

               
            else:               
                flash("Credenziali Errate","error")  
                return render_template('/General/login.html')    
        else:           
            flash("Credenziali Errate","error")  
            return render_template('/General/login.html')   


        
    return  render_template('/General/login.html')


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
        if(name and surname and address and city and email and cellular and password):

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