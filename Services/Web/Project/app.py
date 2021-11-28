from os import name
from flask import Flask, sessions, g, render_template
from config import DATABASE_CONNECTION_URI






    


app = Flask(__name__)


from DbController import db_start,create_db_users
db_start()
create_db_users()



@app.route('/')
def home():  
    from Views.general import general
    from Views.user import user
    from Views.instructor import instructor
    from Views.manager import manager
    # registring blueprints
    app.register_blueprint(general)
    app.register_blueprint(user)
    app.register_blueprint(instructor)
    app.register_blueprint(manager)  
 
    return 'Hello World!'


