from sqlalchemy import (Column,ForeignKey,Integer,String)
from sqlalchemy import create_engine,inspect
from sqlalchemy import or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.orm import with_polymorphic
from sqlalchemy.sql.expression import column, false
from sqlalchemy.sql.sqltypes import (Boolean)
from DbController import Base,session
#from flask_login import UserMixin
from flask_security import UserMixin
from app import bcrypt

#from Lessons import Lesson
#from Reservations import Reservation
#from Roles import Role




class User(UserMixin,Base):

    __tablename__='Users'
 

    id = Column("id",Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column( String(50), nullable=False)
    email = Column(String(40), nullable=False,unique=True)
    address = Column( String(30), nullable=False)
    city = Column(String(30), nullable=False)
    password = Column( String, nullable=False)    
    role = Column(Integer,ForeignKey("Roles.id"),nullable=False,default=3)    
    #is_authenticated = Column( Boolean, default=False, nullable=False)
    #is_active = Column( Boolean, default=False, nullable=False)
    # is_anonymous=Column( Boolean, default=False, nullable=False)

    role_obj=relationship("Role",back_populates="users_obj")

    lessons_obj=relationship("Lesson",back_populates="trainer_obj")
    reservations_obj=relationship("Reservation",back_populates="user_obj")



    def __init__(self,name,surname,email,address,city,password,role):
        self.name=name
        self.surname=surname
        self.email=email 
        self.address=address
        self.city=city
        self.password=bcrypt.generate_password_hash(password).decode("utf-8")
        self.role=role

    def checkpsw(self, password):
        return bcrypt.check_password_hash(self._password, password)

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


    def update_obj(self,name,surname,email,address,city):
        try:
            self.name=name 
            self.surname=surname
            self.email=email
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

    def activate_or_deactivate_obj(self,bool):
        try:
            self.is_active=bool
            session.commit()
            return True
        except:
            session.rollback()
            return False