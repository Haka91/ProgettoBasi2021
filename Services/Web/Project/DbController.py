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
    from Models import Roles,Users

   
    role1=Roles.Role("User")
    role1.add_obj()
    role2=Roles.Role("Trainer")
    role2.add_obj()
    role3=Roles.Role("Admin")
    role3.add_obj()
    adminUser=Users.User("admin","admin","admin@gmail.com","12345","ovunque","behindyou","admin",3)
    adminUser.add_obj()
    trainerUser=Users.User("trainer","trainer","trainer@gmail.com","123456","boh","jesolo","trainer",2)
    trainerUser.add_obj()
    costumerUSer=Users.User("costumer","costumer","costumer@gmail.com","1234556","boh","jesolo","costumer",1)
    costumerUSer.add_obj()
    
     
    try:
        conn.execute("CREATE USER manager WITH password 'manager';")
        conn.execute("CREATE USER trainer WITH password 'trainer';")
        conn.execute("CREATE USER customer WITH password 'customer';")
        conn.execute("CREATE USER anonymous WITH password 'anonymous';")
    except:
        print('figa è esploso tutto') #ti prego ricordati di modificare l'alert 



