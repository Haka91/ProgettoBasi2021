# Blueprint per la sezione user

from flask import Flask
from flask import Blueprint, render_template



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


# DA FARE
#@instructor.route('/creazioneLezioni')