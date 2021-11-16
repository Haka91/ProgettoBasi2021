from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import or_
from sqlalchemy import String

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, relationships
from sqlalchemy.orm import Session
from sqlalchemy.orm import with_polymorphic
from app import Base,engine



class Courses(Base):

    __tablename__='Courses'
 

    id= Column("id",Integer, primary_key=True)
    name = Column(String(50))
    description=Column(String(50))
    trainer = Column(Integer,ForeignKey("Users.id"),nullable=False)

  
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

    
