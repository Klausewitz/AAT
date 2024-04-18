from sqlalchemy import Integer, create_engine, String, ForeignKey, Table, Column
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, relationship, declarative_base
from typing_extensions import Annotated
from typing import List, Set


# __init__


DATABASE = 'database.db'

engine = create_engine(f'sqlite:///AAT/instance/{DATABASE}', echo=False)
Base = declarative_base()


# models
user_module = Table(
    'user_module',
    Base.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('module_id', ForeignKey('module.id'), primary_key=True)
)

class User(Base):

    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False) 
    is_staff: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    modules: Mapped[List['Module']] = relationship(secondary=user_module, lazy=False, back_populates='users')

    def __repr__(self):
        return f'id: {self.id}, name: {self.username}.'
    

class Module(Base):
    __tablename__ = 'module'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    code: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)

    users: Mapped[List['User']] = relationship(secondary=user_module, lazy=False, back_populates='modules')

    def __repr__(self):
        return f'id: {self.id}, module: {self.code} {self.name}.'
      

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# query

# add new 
def new_user_module(user, module):
    user.modules.append(module)
    session.commit()

# delete
def delete_user_module(user, module):    
    user.modules.remove(module)
    session.commit()

# select
def select_user(user_info):
    if type(user_info) == str:
        user = session.query(User).filter(User.username == user_info).scalar()
    else:    
        user = session.query(User).filter(User.id == user_info).scalar()
    return user   


def select_module(module_info):
    if type(module_info) == str:
        module = session.query(Module).filter(Module.code == module_info).scalar()
    else:
        module = session.query(Module).filter(Module.id == module_info).scalar()
    return module 

# select all user modules
def select_user_current_module(user_id: int):
    user = select_user(user_id)
    return user.modules

# select all modules that not assigned to user  
def select_user_other_modules(user_id: int):
    modules_not_assigned = session.query(Module).filter(~Module.users.any(User.id == user_id)).all()
    return modules_not_assigned

def get_all_modules():
    return session.query(Module).all()    

def main():

    '''# CMT group
    staff1 = select_user('staff1')
    student230101 = select_user('student230101')
    student230102 = select_user('student230102')
    student230103 = select_user('student230103')
    student230104 = select_user('student230104')
    CMT313 = select_module('CMT313')
    CMT219 = select_module('CMT219')
    CMT120 = select_module('CMT120')
    
    # MTH group
    staff2 = select_user('staff2')
    student230202 = select_user('student230202')
    student230203 = select_user('student230203')
    student230204 = select_user('student230204')
    MTH322 = select_module('MTH322')
    MTH303 = select_module('MTH303')
    MTH319 = select_module('MTH319')'''
    staff1 = select_user('staff1')
    CCT001 = select_module('CCT001')
    new_user_module(staff1, CCT001)
    


    

    
    




if __name__ == '__main__':
    main()
