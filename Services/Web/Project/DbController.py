from datetime import  datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_CONNECTION_URI





#testing purpose,give it a real name after setting docker compose
Base = declarative_base()

engine = create_engine(DATABASE_CONNECTION_URI)

# create a configured "Session" class
Session = sessionmaker(bind=engine)
 
# create a Session

session = Session()
 
# create all tables that don't yet exist

#se è già creato non 
def db_start_already_loaded():   
    from Models import Courses
    from Models import Days
    from Models import Policies
    from Models import Reservation_Slots
    from Models import Roles
    from Models import Rooms
    from Models import Users
    from Models import Lessons #2
    from Models import Reservations #3    
    Base.metadata.create_all(engine)




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
   
    
    from Models import Roles,Users,Rooms,Policies,Courses,Days,Reservation_Slots,Reservations,Lessons

    #creo ruoli
    print("creo ruoli")
    role1=Roles.Role("User")
    role1.add_obj()
    role2=Roles.Role("Trainer")
    role2.add_obj()
    role3=Roles.Role("Admin")
    role3.add_obj()
    #creo users
    print("creo users")
    adminUser=Users.User("admin","admin","admin@gmail.com","12345","ovunque","behindyou","admin",3)
    adminUser.add_obj()
    trainerUser=Users.User("trainer","trainer","trainer@gmail.com","123456","boh","jesolo","trainer",2)
    trainerUser.add_obj()
    trainerUser2=Users.User("trainer2","trainer","trainer2@gmail.com","12345666","boh","jesolo","trainer",2)
    trainerUser2.add_obj()
    costumerUser=Users.User("costumer","costumer","costumer@gmail.com","1234556","boh","jesolo","costumer",1)
    costumerUser.add_obj()
    costumerUser2=Users.User("costumer2","costumer","costumer2@gmail.com","1234556","boh","jesolo","costumer",1)
    costumerUser2.add_obj()
    costumerUser3=Users.User("costumer3","costumer","costumer3@gmail.com","1234556","boh","jesolo","costumer",1)
    costumerUser3.add_obj()
    costumerUser4=Users.User("costumer4","costumer","costumer4@gmail.com","1234556","boh","jesolo","costumer",1)
    costumerUser4.add_obj()
    costumerUser5=Users.User("costumer5","costumer","costumer5@gmail.com","1234556","boh","jesolo","costumer",1)
    costumerUser5.add_obj()
    costumerUser6=Users.User("costumer6","costumer","costumer6@gmail.com","1234556","boh","jesolo","costumer",1)
    costumerUser6.add_obj()
    costumerUser7=Users.User("costumer7","costumer","costumer7@gmail.com","1234556","boh","jesolo","costumer",1)
    costumerUser7.add_obj()
    costumerUser8=Users.User("costumer8","costumer","costumer8@gmail.com","1234556","boh","jesolo","costumer",1)
    costumerUser8.add_obj()
    costumerUser9=Users.User("costumer9","costumer","costumer9@gmail.com","1234556","boh","jesolo","costumer",1)
    costumerUser9.add_obj()
    print("creo stanze")
    weightRoom=Rooms.Weight_Room("sala pesi","piena di gente alle 7",50)
    weightRoom.add_obj()
    weightRoom2=Rooms.Weight_Room("sala pesi 2","sala pesi 2",30)
    weightRoom2.add_obj()
    weightRoom3=Rooms.Weight_Room("sala pesi 3","sala pesi 3",100)
    weightRoom3.add_obj()
    courseRoom=Rooms.Course_Room("sala corsi Celeste","usata come magazzino di solito",12,True)
    courseRoom.add_obj()
    courseRoom2=Rooms.Course_Room("sala corsi Bianca","sala più piccola,ma che da una sensazione di familiarità",16)
    courseRoom2.add_obj()
    courseRoom2=Rooms.Course_Room("sala corsi Ross","sala enorme,nei weekend balera",100)
    courseRoom2.add_obj()
    print("creo policy")
    standardPolicy=Policies.Policy("default",100,5)
    standardPolicy.add_obj()
    standardPolicy2=Policies.Policy("special",50,3)
    standardPolicy2.add_obj()
    print("creo corsi")
    yogaCourse=Courses.Course("yoga","ultimamente va di moda",trainer=2,maxcostumers=20)
    yogaCourse.isvisible=True
    yogaCourse.add_obj()
    pilatesCourse=Courses.Course("pilates","Corso di Pilates",trainer=3,maxcostumers=20)
    pilatesCourse.isvisible=True
    pilatesCourse.add_obj()
    yogaCourse2=Courses.Course("KickBoxing","entri per fare a pugni,esci che le hai prese",trainer=1,maxcostumers=15)
    yogaCourse2.isvisible=True
    yogaCourse2.add_obj()

    print("creo giorni")
    startDate=(datetime.today()- timedelta(days=36))
    while(startDate<(datetime.today()-timedelta(days=15))):
        today=(startDate.date())
        day=Days.Day(today,datetime(today.year,today.month,today.day,8,30),datetime(today.year,today.month,today.day,16,30),break_slot=0)    
        day.add_obj() 
        startDate=startDate+timedelta(days=1)   

    startDate=(datetime.today()- timedelta(days=14))
    while(startDate<(datetime.today()+timedelta(days=15))):
        today=(startDate.date())
        day=Days.Day(today,datetime(today.year,today.month,today.day,8,30),datetime(today.year,today.month,today.day,15,30),break_slot=3,break_time=datetime(today.year,today.month,today.day,11,30),policy=2)    
        day.add_obj() 
        startDate=startDate+timedelta(days=1)   
    
    
    
    i=1   
    print("prenotazioni in creazione,ci vorrà un po")  
    while i < 704:        
        if(i%60==0):
            u=1
            while u<13:
                r=1
                
                weightReservationToAdd=Reservations.Weight_Room_Reservation(r%3,i,u)
                weightReservationToAdd.add_obj()
                    
                    
                
                u=u+1
        i=i+1
    

    print("create prenotazioni sala pesi")

    q=1   
    print("lezioni in creazione,ci vorrà un po")
    while q < 704:        
        if(q%14==0):
   
                    if(q%3==0):
                        lessonToAdd=Lessons.Lesson(q,1,4)
                        lessonToAdd.add_obj()                   
                        r=r+1
                    elif(q%3==1):
                        lessonToAdd=Lessons.Lesson(q,2,5)
                        lessonToAdd.add_obj()                   
                        r=r+1
                    else:
                        lessonToAdd=Lessons.Lesson(q,3,6)
                        lessonToAdd.add_obj()                   
                        r=r+1
                
           
        q=q+1

    
    print("create lezioni")# 50 lezioni create

    print("prenotazioni lezioni in creazione,ci vorrà un po")

    les=1
    while les<51:

            u=1
            while u<13:
                if((les)%3==0):
                
                    weightReservationToAdd=Reservations.Course_Reservation(les,u)
                    weightReservationToAdd.add_obj()                  
                    
                
                u=u+1
            les=les+1

   
    print("create prenotazioni a lezioni")# 50 lezioni create


    
    conn= engine.connect() 
     
    try:
        #creo solo un utente per la connessione alla mia app,per la spiegazione sul perchè consultare documentazione
        conn.execute("CREATE USER standard WITH password 'standard';")    
        
    except Exception as e:
        print('utente di connessione già creato nel db') 
     
    

    try:
        #so che essendo lo schema PUBLIC ha già di base l'usage,ma se un giorno cambiamo schema e non usiamo public è già pronto      
        conn.execute('GRANT USAGE ON SCHEMA "public" TO standard;')              
    except Exception as e:
        print('privilegi di accesso già dati a standard') 

    try:             
        conn.execute('GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA "public" TO standard;')        
    except Exception as e:
        print(e) 
      
    try:             
        conn.execute('GRANT SELECT, DELETE, INSERT,UPDATE ON TABLE "public"."Courses" TO standard;')        
    except Exception as e:
        print(e) 

  


       
    try:       
        conn.execute('GRANT SELECT, DELETE, INSERT,UPDATE ON TABLE "public"."Days" TO standard;')        
    except Exception as e:       
        print(e) 


    try:      
        conn.execute('GRANT SELECT, DELETE, INSERT,UPDATE ON TABLE "public"."Lessons" TO standard;')        
    except Exception as e:    
        print(e) 



    try:      
        conn.execute('GRANT SELECT, DELETE, INSERT,UPDATE ON TABLE "public"."Policies" TO standard;')        
    except Exception as e:        
        print(e) 



    try:          
        conn.execute('GRANT SELECT, DELETE, INSERT,UPDATE ON TABLE "public"."Reservation_slots" TO standard;')        
    except Exception as e:
        print(e) 


    
    try:         
        conn.execute('GRANT SELECT, DELETE, INSERT,UPDATE ON TABLE "public"."Reservations" TO standard;')        
    except Exception as e:     
        print(e) 



    try:         
        conn.execute('GRANT SELECT, DELETE, INSERT,UPDATE ON TABLE "public"."Weight_Room_Reservations" TO standard;')        
    except Exception as e:     
        print(e) 



    try:         
        conn.execute('GRANT SELECT, DELETE, INSERT,UPDATE ON TABLE "public"."Course_Reservations" TO standard;')        
    except Exception as e:     
        print(e) 



    try: 
        #nonostante sia un solo user per tutti non voglio che nessuno possa inserire e rimuovere Roles,quelle  DEVONO essere fisse      
        conn.execute('GRANT SELECT ON TABLE "public"."Roles" TO standard;')        
    except Exception as e:      
        print(e) 



    try:             
        conn.execute('GRANT SELECT, DELETE, INSERT,UPDATE ON TABLE "public"."Rooms" TO standard;')        
    except Exception as e:      
        print(e) 


    
    try:             
        conn.execute('GRANT SELECT, DELETE, INSERT,UPDATE ON TABLE "public"."Course_Rooms" TO standard;')        
    except Exception as e:      
        print(e) 



    try:             
        conn.execute('GRANT SELECT, DELETE, INSERT,UPDATE ON TABLE "public"."Weight_Rooms" TO standard;')        
    except Exception as e:      
        print(e) 



    try:           
        conn.execute('GRANT SELECT, DELETE, INSERT,UPDATE ON TABLE "public"."Users" TO standard;')        
    except Exception as e:        
        print(e)  




