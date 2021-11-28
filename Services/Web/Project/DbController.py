from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from config import DATABASE_CONNECTION_URI



#testing purpose,give it a real name after setting docker compose
Base = declarative_base()

engine = create_engine(DATABASE_CONNECTION_URI)

# create a configured "Session" class
Session = sessionmaker(bind=engine)
 
# create a Session

session = Session()
 
# create all tables that don't yet exist







def db_start():   
    from Models import Courses
    from Models import Days
    from Models import Policies
    from Models import Reservation_Slots
    from Models import Roles
    from Models import Rooms
    from Models import Users
    from Models import Lessons #2
    from Models import Reservations #3
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def create_db_users():
    conn= engine.connect()
    try:
        conn.execute("CREATE USER manager WITH password 'manager';")
        conn.execute("CREATE USER trainer WITH password 'trainer';")
        conn.execute("CREATE USER customer WITH password 'customer';")
        conn.execute("CREATE USER anonymous WITH password 'anonymous';")
    except:
        print('figa è esploso tutto') #ti prego ricordati di modificare l'alert 

