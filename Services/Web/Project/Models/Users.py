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

from app import Base,engine



class Users(Base):

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
    is_authenticated = Column( Boolean, default=False, nullable=False)
    is_activated = Column( Boolean, default=False, nullable=False)

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



