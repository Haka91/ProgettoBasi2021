from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from DbController import Base,session




class Role(Base):

    __tablename__='Roles'
   

    id = Column("id",Integer, primary_key=True)
    name = Column(String(50))

    users_obj=relationship("User",back_populates="role_obj", cascade="all, delete")

    def __init__(self,name):
        self.name=name
        

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
 
    def update_obj(self, name):
        try:
            self.name=name                    
            session.commit()
            return True
        except:
            session.rollback()
            return False



