from os import name
from flask import Flask, sessions, g, render_template
from sqlalchemy.dialects import postgresql
import psycopg2
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy.sql.functions import user
from config import DATABASE_CONNECTION_URI


# import blueprints (between from and import goes the name of the folders)
from .Views.general import general
from .Views.user import user
from .Views.instructor import instructor
from .Views.manager import manager


#testing purpose,give it a real name after setting docker compose
Base=declarative_base()

engine = create_engine(DATABASE_CONNECTION_URI)

#Base.metadata.reflect(bind=engine)

# create a configured "Session" class
Session = sessionmaker(bind=engine)
 
# create a Session
session = Session()
 
# create all tables that don't yet exist

from Models import Courses
from Models import Days
from Models import Policies
from Models import Reservation_Slots
from Models import Roles
from Models import Rooms
from Models import Users
from Models import Lessons #2
from Models import Reservations #3


Base.metadata
#Base.metadata.drop_all(engine)
#Base.metadata.create_all(engine)



conn= engine.connect()
conn.execute("CREATE USER admin WITH password 'standard';")
    





app = Flask(__name__)



@app.route('/')
def home():    
    # registring blueprints
    app.register_blueprint(general)
    app.register_blueprint(user)
    app.register_blueprint(instructor)
    app.register_blueprint(manager)
    return 'Hello World!'
