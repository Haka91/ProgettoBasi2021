# Blueprint per la sezione user

from flask import Flask
from flask import Blueprint, render_template, redirect, url_for
from flask.helpers import url_for
from flask_login import current_user



instructor = Blueprint('instructor',__name__,url_prefix='/instructor')


@instructor.route('/introduzione')
def introduzione():
    # mi serve una query:
    # 1) lista dei corsi attivi in cui insegna con numero di persone iscritte per ogni corso ( nome corso , numero iscritti )
    # 2) lista delle lezioni di questa settimana ( nome corso , locale , dataOraInizio , dataOraFine , numero prenotati ) 
    return render_template('/Instructor/introduzione.html') # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE

  
@instructor.route('/prossimeLezioni')
def prossimeLezioni():
    # mi serve una query:
    # 1) lista con tutte le lezioni che l'istruttore deve fare ( nome corso , locale , dataOraInizio , dataOraFine , numero prenotati )
    return render_template('/Instructor/prossimeLezioni.html') # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE


@instructor.route('/creaLezioni')
def creaLezioni():
    # mi serve una query:
    # 1) lista con tutti i corsi che l'istruttore insegna ( nome corso )
    return render_template('/Instructor/creaLezioni.html')

# METODO PER INSERIRE LE LEZIONI NEL DB, IL METODO VA POI AGGIUNTO NEL FORM CHE SI TROVA NELL'HTML (PRE SPECIFICARE L'AZIONE DEL FORM)
@instructor.route('/inserisciLezioni', methods = ['POST', 'GET'])
def inserisciLezioni():
    # INSERIRE LE LEZIONI NEL DB
    return redirect(url_for(instructor.prossimeLezioni))  # ridirezione l'istruttore, dopo l'inserimento delle lezioni, verso la lista delle sue lezioni da fare
