from flask import Flask
from datetime import timedelta
import os
from config import secret_key
from flask_bcrypt import Bcrypt




app = Flask(__name__)
app.secret_key=secret_key
#aggiungiamo un limite alla sessione per alcuni comportamenti incorretti di rememberme di flaskLogin con chrome
app.permanent_session_lifetime =timedelta(minutes=30)
#we initialize Bcrypt
bcrypt = Bcrypt(app)

#we initialize the flask-login
from flask_login import LoginManager


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view=""
login_manager.session_protection = "strong"




from DbController import db_start,create_db_users,db_start_already_loaded
#cambio l'user se è già creato il db
if( not os.environ['POSTGRES_USER']=="postgres"):
    db_start_already_loaded()
else:
    db_start()
    create_db_users()
    os.environ['POSTGRES_USER']="standard"
    os.environ['POSTGRES_PASSWORD']="standard"


from general import general
from user import user
from instructor import instructor
from manager import manager
# registro le blueprints
app.register_blueprint(general)
app.register_blueprint(user)
app.register_blueprint(instructor)
app.register_blueprint(manager)  


"""
@app.route('/')
def home():  
    from Models import Roles,Users,Rooms

    
    role=Roles.Role("Admin")
    role.add_obj()
    
    print(role.id,role.name)
    ale=Users.User("ale","furlan","ale@gmail.com","via giacomo","jesolo","ciao",1)    
    ale.add_obj()
    print(ale.role_obj,ale.name,ale.id)
    room=Rooms.Weight_Room("pesi","salapesi",100)
    room2=Rooms.Course_Room("room","ciao",100)
    room.add_obj()
    room2.add_obj()
    return redirect(url_for(general.homepage))
"""


