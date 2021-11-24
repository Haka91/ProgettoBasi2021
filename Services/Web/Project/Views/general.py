#primo file per la prima blueprint. Questa blueprint sarà per le pagine senza login e per la pagina di login e registrazione

# ho copiato a caso gli import che avevi messo su app.py + alcune aggiunte [CAPIRO' COSA FARE ESATTAMENTE]
from os import name
from flask import Flask, sessions, Blueprint, render_template
from sqlalchemy.dialects import postgresql
import psycopg2
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy.sql.functions import user
from config import DATABASE_CONNECTION_URI


mod = Blueprint('General',__name__)


# homepage
@mod.route('/')
def index():
    # mi servono due query:
    # 1) lista dei corsi (nome corso, nome istruttore, data inizio, data fine)  
    # 2) lista delle sale (nome sala, capienza)  
    # ---
    # Secondo te inseriamo pure gli orari di apertura e chiusura?
    return render_template('/General/homepage.html') # UNA VOLTA PRESENTI LE QUERY PASSARE I DATI AL TEMPLATE


# login page
@mod.route('/loginPage')
def loginPage():
    return render_template('/General/login.html')


# login function
@mod.route('/loginFunzione')
def loginFunzione():
    # do stuff
    return 


# register page
@mod.route('/registerPage')
def registerPage():
    return render_template('/General/register.html')


# register function
@mod.route('/registerFunction')
def registerFunction():
    # do stuff
    return