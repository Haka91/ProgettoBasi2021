from os import name
from flask import Flask, sessions, g, render_template
from config import DATABASE_CONNECTION_URI

from general import general
from user import user
from instructor import instructor
from manager import manager


from DbController import db_start,create_db_users
db_start()
create_db_users()

    


app = Flask(__name__)
# registring blueprints
app.register_blueprint(general)
app.register_blueprint(user)
app.register_blueprint(instructor)
app.register_blueprint(manager)  




@app.route('/')
def home():  
    
    
 
    return 'Hello World!'


