from datetime import date, datetime, timedelta
from flask.helpers import flash
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import or_
from sqlalchemy import String
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.schema import CheckConstraint
from sqlalchemy import (String,DateTime,Date,Time)


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
    isvisible = Column(Boolean,default=False)
    maxcostumers= Column(Integer,CheckConstraint('maxcostumers<101'),CheckConstraint('maxcostumers>0'),nullable=False,default=100)


    lessons_obj= relationship("Lesson",back_populates="course_obj", cascade="all, delete")
    trainer_obj= relationship("User", back_populates="courses_obj")
   
    
    def __init__(self,name,description,trainer,maxcostumers=100):
        self.trainer=trainer
        self.name=name,
        self.description=description
        self.isvisible=False
        self.maxcostumers=maxcostumers

    def activate_or_deactivate_obj(self):
        if len(self.lessons_obj)>0:
            try:
                self.isvisible=not self.isvisible            
                session.commit()
                return True
            except:
                session.rollback()
                return False
        else:
            flash("non puoi rendere visibile un corso senza lezioni")
            return False

    def numberofLesson(self):
        return len(self.lessons_obj)

  
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

    def isDeletable(self):
        deletable=True
        if len(self.lessons_obj)==0:
            return deletable
        else:
            for lesson in self.lessons_obj:
               if(lesson.reservation_slot_obj.day >(date.today()- timedelta(days=30))):
                   deletable=False
        return deletable

