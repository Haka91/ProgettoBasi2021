
from sqlalchemy import (Column,ForeignKey,Integer,String)
from sqlalchemy.orm import relationship
from DbController import Base,session
from flask_login import UserMixin,current_user
from werkzeug.utils import redirect
from functools import wraps
from flask.helpers import url_for,flash
from app import bcrypt,login_manager






class User(UserMixin,Base):

    __tablename__='Users'
 

    id = Column("id",Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column( String(50), nullable=False)
    email = Column(String(40), nullable=False,unique=True)
    cellular=Column(String(40), nullable=False)
    address = Column( String(30), nullable=False)
    city = Column(String(30), nullable=False)
    password = Column( String, nullable=False)    
    role = Column(Integer,ForeignKey("Roles.id"),nullable=False,default=3)
     
  

    role_obj=relationship("Role",back_populates="users_obj")

    courses_obj=relationship("Course",back_populates="trainer_obj",cascade="all, delete")
    reservations_obj=relationship("Reservation",back_populates="user_obj",cascade="all, delete")



    def __init__(self,name,surname,email,cellular,address,city,password,role):
        self.name=name
        self.surname=surname
        self.email=email 
        self.cellular=cellular
        self.address=address
        self.city=city
        self.password=bcrypt.generate_password_hash(password).decode("utf-8")
        self.role=role
        

    def checkpsw(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def add_obj(self):

            try:
                session.add(self)
                session.commit()              
                return True
            except Exception as e:
                print(e)
                session.rollback()
                return False

    def delete_obj(self):
       
            try:
                session.delete(self)
                session.commit()
                return True
            except:
               session.rollback()
               return False


    def update_obj(self,name,surname,cellular,address,city):
        try:          
            
            self.name=name 
            self.surname=surname                
            self.cellular=cellular
            self.address=address
            self.city=city             
            session.commit()
            return True
        
        except:
            session.rollback()
            return False


    def update_password(self,old_password,new_password):
        try:
            if(self.checkpsw(old_password)):
                self.password=bcrypt.generate_password_hash(new_password).decode("utf-8")
                session.commit()
                return True
            else:
                return False

        except:
            session.rollback()
            return False

    def update_role(self,role):
        try:
            self.role=role
            session.commit()
            return True
        except:            
            session.rollback()
            return False


    def get_role(self):
        try:
            return self.role
        except:
            
            return 0



#metodo richiesto da FLASK-LOGIN 

@login_manager.user_loader
def load_user(id_user):
    try:
        return session.query(User).get(id_user)       
    except:
        None





#dobbiamo inserire qui le funzioni per evitare i circular import
#qui forzo la selezione della Role uguale all'admin,se creassimo una nuova role avrebbe più' poteri di admin 
def at_least_manager_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_anonymous:
            if current_user.get_role() == 3 :
                return f(*args, **kwargs)
            else:
                flash("ERROR 404 PAGE NOT FOUND","error")

                return redirect(url_for("general.index"))
        else:
            flash("ERROR 404 PAGE NOT FOUND","error")
            return redirect(url_for("general.index"))

    return wrapper





def at_least_trainer_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_anonymous:
            if current_user.get_role() >= 2:
                return f(*args, **kwargs)
            else:
                flash("ERROR 404 PAGE NOT FOUND","error")
                return redirect(url_for("general.index"))
        else:
            flash("ERROR 404 PAGE NOT FOUND","error")
            return redirect(url_for("general.index"))

    return wrapper




def at_least_user_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_anonymous:
            if current_user.get_role() >= 1:
                return f(*args, **kwargs)
            else:
                flash("ERROR 404 PAGE NOT FOUND","error") 
                return redirect(url_for("general.index"))
        else:
            flash("ERROR 404 PAGE NOT FOUND","error") 
            return redirect(url_for("general.index"))

    return wrapper