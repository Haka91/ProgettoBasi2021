# Blueprint per la sezione user

from flask import Flask
from flask import Blueprint, render_template



manager = Blueprint('manager',__name__,url_prefix='/manager')

# AGGIUNGERE LINK PER OGNI UTENTE PER FARE IN MODO DI MODIFICARE IL SUO STATO DI ATTIVATO O NON ATTIVATO
@manager.route('/gestioneUtenti')
def gestioneUtenti():
    # mi serve una query:
    # 1) lista di tutti gli utenti ( ruolo , nome, cognome , attivato/nonAttivato )
    return render_template('/Manager/gestioneUtenti.html') # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE


@manager.route('/gestioneSale')
def gestioneSale():
    # mi serve una query:
    # 1) lista di tutte le sale ( nomeSala , capienza )
    return render_template('/Manager/gestioneSale.html') # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE


@manager.route('/gestioneTrainers')
def gestioneTrainers():
    # mi serve una query:
    # 1) lista di tutti i trainers ( nome , cognome , attivatoNonAttivato , allenaCorsi? (true oppure false) )
    # 2) lista di tutti gli utenti che non sono trainers oppure che non è il gestore ( nome, cognome , attivato/nonAttivato )
    return render_template('/Manager/gestioneTrainers.html') # UNA VOLTA PRESENTE LA QUERY PASSARE I DATI AL TEMPLATE


# DA FARE:  PAGINA STATISTICHE (?)