# Blueprint per la sezione user

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


mod = Blueprint('User',__name__)


@mod.route('/User/introduzione')
def introduzione():
    # mi serve una query:
    # 1) lista delle prenotazioni di questa settimana, sia per i corsi sia per la sala pesi ( nome corso (se sala pesi, scrivere sala pesi) , istruttore ,  locale in cui si svolge , data ed ora inizio , data ed ora fine )
    return render_template('/User/introduzione.html') # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE


@mod.route('/User/prenotazioniAttive')
def prenotazioniAttive():
    # mi serve una query:
    # 1) lista di tutte le le prenotazioni, sia per i corsi sia per la sala pesi ( nome corso (se sala pesi, scrivere sala pesi) , istruttore , locale in cui si svolge , data ed ora inizio , data ed ora fine )
    return render_template('/User/prenotazioniAttive.html') # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE


# DA COMPLETARE PERCHE' MANCA LA POSSIBILITA' EFFETTIVA DI PRENOTARE
@mod.route('/User/prenotaSalaPesi')
def prenotaSalaPesi():
    # mi serve una query:
    # 1) lista degli slot disponibili della prossima settimana / due settimane
    return render_template('/User/prenotaSalaPesi.html') # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE


@mod.route('/User/iscrizioneAiCorsi')
def iscrizioneAiCorsi():
    # mi serve una query:
    # 1) lista degi corsi a cui l'utente in questione non è ancora iscritto
    return render_template('/User/iscrizioneAiCorsi.html') # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE


@mod.route('/User/prenotaLezioneCorso')
def prenotaLezioneCorso():
    # mi serve una query:
    # 1) lista delle lezioni dei corsi a cui l'utente è già iscritto ( nomeCorso , istruttore , locale , dataOraInizio , dataOraFine )
    return render_template('/User/prenotaLezioneCorso.html') # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE


@mod.route('/User/cambiaDatiUtente')
def cambiaDatiUtente():
    # mi serve una query:
    # 1) QUERY CHE MI RITORNA TUTTI I DATI DELL'UTENTE
    return render_template('/User/cambiaDatiUtente.html') # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE