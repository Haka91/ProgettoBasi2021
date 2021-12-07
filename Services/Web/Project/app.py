from os import name
from flask import Flask, sessions, g, render_template
from flask.helpers import url_for
from werkzeug.utils import redirect
from config import DATABASE_CONNECTION_URI,secret_key
from flask_login import LoginManager
from flask_bcrypt import Bcrypt






    


app = Flask(__name__)

app.secret_key=secret_key

from DbController import db_start,create_db_users
#we initialize Bcrypt
bcrypt = Bcrypt(app)

#we initialize the flask-login
login_manager = LoginManager()
#login_manager.init_app(app)
login_manager.session_protection = "strong"

db_start()
create_db_users()


from general import general
from user import user
from instructor import instructor
from manager import manager
# registring blueprints
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

