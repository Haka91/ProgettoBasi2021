#Questa blueprint sarà per le pagine senza login e per la pagina di login e registrazione

from flask import Flask
from flask import Blueprint, render_template


general = Blueprint('general',__name__,url_prefix='/general')


# homepage
@general.route('/')
def index():
    # mi servono due query:
    # 1) lista dei corsi (nome corso, nome istruttore, data inizio, data fine)  
    # 2) lista delle sale (nome sala, capienza)  
    # ---
    # Secondo te inseriamo pure gli orari di apertura e chiusura?
    return render_template('/General/homepage.html') # UNA VOLTA PRESENTI LE QUERY PASSARE I DATI AL TEMPLATE


# login page
@general.route('/loginPage')
def loginPage():
    return "negro"#render_template('/General/login.html')


# login function
@general.route('/loginFunzione')
def loginFunzione():
    # do stuff
    return 


# register page
@general.route('/registerPage')
def registerPage():
    return render_template('/General/register.html')


# register function
@general.route('/registerFunction')
def registerFunction():
    # do stuff
    return