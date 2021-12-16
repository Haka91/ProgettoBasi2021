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
from sqlalchemy.sql.sqltypes import Boolean
from DbController import Base,session
#from Models.Lessons import Lesson





class Course(Base):

    __tablename__='Courses'
 

    id= Column("id",Integer, primary_key=True)
    name = Column(String(50))
    description=Column(String(50))    
    trainer = Column(Integer,ForeignKey("Users.id"),nullable=False)
    isActive = Column(Boolean,default=True)


    lessons_obj= relationship("Lesson",back_populates="course_obj")
    trainer_obj= relationship("User", back_populates="courses_obj")
   
    
    def __init__(self,name,description,trainer):
        self.trainer=trainer
        self.name=name,
        self.description=description
        self.isActive=True

    def activate_or_deactivate_obj(self):
        try:
            self.isActive=not self.isActive
            session.commit()
            return True
        except:
            session.rollback()
            return False


  
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

    def update_obj(self, name ,description):
        try:
            self.name=name
            self.description = description           
            session.commit()
            return True
        except:
            session.rollback()
            return False
