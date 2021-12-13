# Blueprint per la sezione user

from flask import Flask
from flask import Blueprint, render_template
from DbController import session
from Models.Users import User,at_least_manager_required
from Models.Policies import Policy
from Models.Rooms import Weight_Room,Course_Room,Room
from Models.Reservations import Reservation



user = Blueprint('user',__name__,url_prefix='/user')


@user.route('/introduzione')
def introduzione():
    prenotazioni=session.query(Reservation)
    return render_template('/User/introduzione.html', prenotazioni=prenotazioni)


@user.route('/prenotazioniAttive')
def prenotazioniAttive():
    # mi serve una query:
    # 1) lista di tutte le le prenotazioni, sia per i corsi sia per la sala pesi ( nome corso (se sala pesi, scrivere sala pesi) , istruttore , locale in cui si svolge , data ed ora inizio , data ed ora fine )
    return render_template('/User/prenotazioniAttive.html') # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE


# DA COMPLETARE PERCHE' MANCA LA POSSIBILITA' EFFETTIVA DI PRENOTARE
@user.route('/prenotaSalaPesi')
def prenotaSalaPesi():
    # mi serve una query:
    # 1) lista degli slot disponibili della prossima settimana / due settimane
    return render_template('/User/prenotaSalaPesi.html') # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE


@user.route('/iscrizioneAiCorsi')
def iscrizioneAiCorsi():
    # mi serve una query:
    # 1) lista degi corsi a cui l'utente in questione non è ancora iscritto (idCorso,nomeCorso)
    return render_template('/User/iscrizioneAiCorsi.html') # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE


@user.route('/prenotaLezioneCorso')
def prenotaLezioneCorso():
    # mi serve una query:
    # 1) lista delle lezioni dei corsi a cui l'utente è già iscritto ( nomeCorso , istruttore , locale , dataOraInizio , dataOraFine )
    return render_template('/User/prenotaLezioneCorso.html') # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE


@user.route('/cambiaDatiUtente')
def cambiaDatiUtente():
    # mi serve una query:
    # 1) QUERY CHE MI RITORNA TUTTI I DATI DELL'UTENTE
    return render_template('/User/cambiaDatiUtente.html') # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE