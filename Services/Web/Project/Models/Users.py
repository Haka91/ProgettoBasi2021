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
from DbController import Base,engine
#from flask_login import UserMixin
from flask_security import UserMixin
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
    salt=Column(String,nullable=false)
    role = Column(Integer,ForeignKey("Roles.id"),nullable=False,default=3)    
    #is_authenticated = Column( Boolean, default=False, nullable=False)
    #is_active = Column( Boolean, default=False, nullable=False)
    # is_anonymous=Column( Boolean, default=False, nullable=False)

    role_obj=relationship("Role",back_populates="users_obj")

    lessons_obj=relationship("Lesson",back_populates="trainer_obj")
    reservations_obj=relationship("Reservation",back_populates="user_obj")
    def add_obj(self):

            try:
                engine.session.add(self)
                engine.session.commit()
                return True
            except Exception as e:
                print(e)
                engine.session.rollback()
                return False

    def delete_obj(self):
       
            try:
                engine.session.delete(self)
                engine.session.commit()
                return True
            except:
               engine.session.rollback()
               return False


    def update_obj(self,name,surname,email,address,city,password,role):
        try:
            self.name=name 
            self.surname=surname
            self.email=email
            self.address=address
            self.city=city             
            engine.session.commit()
            return True
        except:
            engine.session.rollback()
            return False


    def update_password(self,password):
        try:
            #usa password+salt
            engine.session.commit()
            return True
        except:
            engine.session.rollback()
            return False

    def update_role(self,role):
        try:
            self.role=role
            engine.session.commit()
            return True
        except:
            engine.session.rollback()
            return False