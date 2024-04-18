import bcrypt
from datetime import datetime
from flask_login import UserMixin, login_user
from routes import db, login_manager
from typing import List
from sqlalchemy import Integer, String, Select, ForeignKey, Table, Column, MetaData, TIMESTAMP, BLOB
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


# association table
user_module = Table(
    'user_module', db.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('module_id', ForeignKey('module.id'), primary_key=True)
)


class User(db.Model, UserMixin):

    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False) 
    is_staff: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    modules: Mapped[List['Module']] = relationship(secondary=user_module, lazy=False, back_populates="users")

    def __repr__(self):
        return f'id: {self.id}, username: {self.username}, is staff? {self.is_staff}, year: {self.year}.'
    

    # check if input psw == database psw
    def check_psw(self, input_psw):
        hashed_psw = self.password.encode()
        return bcrypt.checkpw(input_psw.encode(), hashed_psw)
    

class Module(db.Model):

    __tablename__ = 'module'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(String, nullable=False) 
    
    users: Mapped[List['User']] = relationship(secondary=user_module, lazy=False, back_populates="modules")
    assignments: Mapped[List['Assignment']] = relationship(back_populates='module')
    mcqs: Mapped[List['Mcq']] = relationship(back_populates='module') 
    tfs: Mapped[List['Tf']] = relationship(back_populates='module')

    def __repr__(self):
        return f'module: {self.code} {self.name}.'
    

assignment_question = Table(
    'assignment_question', db.metadata,
    Column('assignment_id', ForeignKey('assignment.id'), primary_key=True),
    Column('is_mcq'),
    Column('mcq_id', ForeignKey('mcq.id')),
    Column('tf_id', ForeignKey('tf.id'))
)


class Assignment(db.Model):  # not finished, is_open -> open & close, duration, max_attempts, etc...

    __tablename__ = 'assignment'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    module_id: Mapped[int] = mapped_column(Integer, ForeignKey('module.id'), nullable=False)
    is_open: Mapped[int] = mapped_column(Integer, nullable=False)
    max_attempts: Mapped[int] = mapped_column(Integer, nullable=False)

    module: Mapped[Module] = relationship(lazy=False, back_populates='assignments')
    mcqs: Mapped[List['Mcq']] = relationship(secondary=assignment_question, lazy=False, back_populates="assignments", overlaps="tfs") 
    tfs: Mapped[List['Tf']] = relationship(secondary=assignment_question, lazy=False, back_populates="assignments", overlaps="mcqs") # overlaps="mcqs"

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}.'
    

class Mcq(db.Model):

    __tablename__ = 'mcq'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    module_id: Mapped[int] = mapped_column(Integer, ForeignKey('module.id'), nullable=False)
    tag: Mapped[str] = mapped_column(String, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    point: Mapped[int] = mapped_column(Integer, nullable=False)
    question: Mapped[str] = mapped_column(String, nullable=False)
    option1: Mapped[str] = mapped_column(String, nullable=False)
    option2: Mapped[str] = mapped_column(String, nullable=False)
    option3: Mapped[str] = mapped_column(String, nullable=False)
    option4: Mapped[str] = mapped_column(String, nullable=False)
    option5: Mapped[str] = mapped_column(String, nullable=False)
    corr_answer: Mapped[str] = mapped_column(String, nullable=False)

    module: Mapped[Module] = relationship(lazy=False, back_populates='mcqs')
    assignments: Mapped[List['Assignment']] = relationship(secondary=assignment_question, lazy=False, back_populates="mcqs", viewonly=True)

    def __repr__(self):
        return f'(mcq) {self.question}'


class Tf(db.Model):

    __tablename__ = 'tf'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    module_id: Mapped[int] = mapped_column(Integer, ForeignKey('module.id'), nullable=False)
    tag: Mapped[str] = mapped_column(String)
    difficulty: Mapped[int] = mapped_column(Integer)
    point: Mapped[int] = mapped_column(Integer, nullable=False)
    __question: Mapped[bytes] = mapped_column(BLOB, name='question', nullable=False)
    corr_answer: Mapped[int] = mapped_column(Integer, nullable=False)

    module: Mapped[Module] = relationship(lazy=False, back_populates='tfs')
    assignments: Mapped[List['Assignment']] = relationship(secondary=assignment_question, lazy=False, back_populates="tfs", viewonly=True)

    @property
    def question(self):
        return self.__question.decode('utf-8')
    
    @question.setter
    def question(self, question_value: str):
        self.__question = question_value.encode()

    def __repr__(self):
        return f'(tf) {self.question}'    
   

class UserService:


    # login 
    def login_action(self, username, password):
        # search from database
        user_db = db.session.query(User).filter(User.username == username).scalar() 
        # if there exist user and psw correct
        if user_db and user_db.check_psw(password):
            # put user into section
            login_user(user_db)
            return True
        return False
    
    
    # get an user by accepting id
    def get_user(self, id):
        return db.session.get(User, id)
    

    # get all users
    def get_all_users(self):
        return db.session.query(User).all()   
    

    # create new user
    def new_user(self, user: User):
        db.session.add(user)
        db.session.commit()
        return user
    

    # change information
    def edit_user(self, user: User, is_staff, year):
        user.is_staff = is_staff
        user.year = year
        db.session.commit()
        return user


    # change password
    def change_password(self, current_user: User, password):
        current_user.password = password
        db.session.commit()
        return current_user
    
    
    # delete user
    def delete_user(self, user_id):
        if type(user_id) == str:
            user_id = int(user_id)
        user = db.session.get(User, user_id)    
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        else:
            return False 

    ############################ user_module #############################

    # add user module permission     
    def new_user_module(self, user, module):
        try:
            user.modules.append(module)
            db.session.commit()
            return True
        except:
            return False
        

    # add user module permissions     
    def new_user_modules(self, user, modules):
        try:
            user.modules.extend(modules)
            db.session.commit()
            return True 
        except:
            return False


    # get user all current modules
    def get_all_current_modules(self, user_info):
        if type(user_info) == User:
            return user_info.modules
        else:
            try:
                user_info = int(user_info)
                user = db.session.query(User).filter(User.id == user_info).scalar()  
            except:
                user = db.session.query(User).filter(User.username == user_info).scalar()
        modules = user.modules
        return modules
    

    # get all modules that not assigned to user  
    def get_user_other_modules(self, user_id):
        modules_not_assigned = db.session.query(Module).filter(~Module.users.any(User.id == user_id)).all()
        return modules_not_assigned
       

    # delete user module permission
    def delete_user_module(self, user, module):
        try:    
            user.modules.remove(module) 
            db.session.commit()
            return True
        except:
            return False


class ModuleService:
    
    
    # get a module by accepting id
    def get_module(self, id):
        return db.session.get(Module, id)
    

    # get all modules
    def get_all_modules(self):
        return db.session.query(Module).all()   

    # create new module
    def new_module(self, module: Module):
        db.session.add(module)
        db.session.commit()
        return module
    
    
    # edit module information
    def edit_module(self, module: Module):
        exist_module = db.session.get(Module, module.id)
        if not exist_module:
            return module
        exist_module.name = module.name
        exist_module.code = module.code
        db.session.commit()
        return module

    
    # delete module
    def delete_module(self, module_id):
        if type(module_id) == str:
            module_id = int(module_id)
        module = db.session.get(Module, module_id)    
        if module:
            db.session.delete(module)
            db.session.commit()
            return True
        else:
            return False 


class AssignmentService:

    # get an assignment by accepting id
    def get_assignment(self, id):
        return db.session.get(Assignment, id)
    

    def get_module_assignment(self, module: Module):
        return module.assignments


    def new_assignment(self, assignment: Assignment):
        db.session.add(assignment)
        db.session.commit()
        return assignment
    
   
    def edit_assignment(self, assignment: Assignment):
        exist_assignment = db.session.get(Assignment, assignment.id)
        if not exist_assignment:
            return assignment
        exist_assignment.name = assignment.name
        # exist_assignment.module_id = assignment.module_id
        exist_assignment.is_open = assignment.is_open
        exist_assignment.max_attempts = assignment.max_attempts
        db.session.commit()
        return assignment

    
    def delete_assignment(self, id):
        if type(id) == str:
            id = int(id)
        assignment = db.session.get(Assignment, id)    
        if assignment:
            db.session.delete(assignment)
            db.session.commit()
            return True
        else:
            return False   

    ############################ assignment_question #############################

    # add question into assignment   
    def new_assignment_mcq(self, assignment, mcq):
        try:
            assignment.mcqs.append(mcq)
            db.session.commit()
            return True
        except:
            return False
    def new_assignment_tf(self, assignment, tf):
        try:
            assignment.tfs.append(tf)
            db.session.commit()
            return True
        except:
            return False
        

    # add questions into assignment 
    def new_assignment_mcqs(self, assignment, mcqs):
        try:
            assignment.mcqs.extend(mcqs)
            db.session.commit()
            return True 
        except:
            return False 
    def new_assignment_tfs(self, assignment, tfs):
        try:
            assignment.tfs.extend(tfs)
            db.session.commit()
            return True 
        except:
            return False 


    # get assignment all current questions
    def get_all_current_mcqs(self, assignment):
        if type(assignment) == Assignment:
            return assignment.mcqs
        else:
            assignment = int(assignment)
            assignment = db.session.query(Assignment).filter(Assignment.id == assignment).scalar()  
        mcqs = assignment.mcqs
        return mcqs
    def get_all_current_tfs(self, assignment):
        if type(assignment) == Assignment:
            return assignment.tfs
        else:
            assignment = int(assignment)
            assignment = db.session.query(Assignment).filter(Assignment.id == assignment).scalar()  
        tfs = assignment.tfs
        return tfs
    

    # get all questions that not assigned to current assignment 
    ''' 这是模板
    def get_user_other_modules(self, user_id):
        modules_not_assigned = db.session.query(Module).filter(~Module.users.any(User.id == user_id)).all()
        return modules_not_assigned
    '''
    def get_assignment_other_mcqs(self, assignment_id):
        mcqs_not_assigned = db.session.query(Mcq).filter(~Mcq.assignments.any(Assignment.id == assignment_id)).all()
        return mcqs_not_assigned
    def get_assignment_other_tfs(self, assignment_id):
        tfs_not_assigned = db.session.query(Tf).filter(~Tf.assignments.any(Assignment.id == assignment_id)).all()
        return tfs_not_assigned
       

    # delete question from assignment
    def delete_assignment_mcq(self, assignment, mcq):
        try:    
            assignment.mcqs.remove(mcq) 
            db.session.commit()
            return True
        except:
            return False   
    def delete_assignment_tf(self, assignment, tf):
        try:    
            assignment.tfs.remove(tf) 
            db.session.commit()
            return True
        except:
            return False            


class QuestionService:

    # get a question by accepting id
    def get_mcq(self, id):
        return db.session.get(Mcq, id)
    def get_tf(self, id):
        return db.session.get(Tf, id)
    

    # get all questions
    def get_all_mcqs(self):
        return db.session.query(Mcq).all()   
    def get_all_tfs(self):
        return db.session.query(Tf).all()   


    # add new question
    def new_mcq(self, mcq: Mcq):
        db.session.add(mcq)
        db.session.commit()
        return mcq
    def new_tf(self, tf: Tf):
        db.session.add(tf)
        db.session.commit()
        return tf
    
    
    # edit module information
    def edit_mcq(self, mcq: Mcq):
        exist_mcq = db.session.get(Mcq, mcq.id)
        if not exist_mcq:
            return mcq
        exist_mcq.tag = mcq.tag
        exist_mcq.difficulty = mcq.difficulty
        exist_mcq.point = mcq.point
        exist_mcq.question = mcq.question
        exist_mcq.option1 = mcq.option1
        exist_mcq.option2 = mcq.option2
        exist_mcq.option3 = mcq.option3
        exist_mcq.option4 = mcq.option4
        exist_mcq.option5 = mcq.option5
        exist_mcq.corr_answer = mcq.corr_answer
        db.session.commit()
        return mcq
    def edit_tf(self, tf: Tf):
        exist_tf = db.session.get(Tf, tf.id)
        if not exist_tf:
            return tf
        exist_tf.tag = tf.tag
        exist_tf.difficulty = tf.difficulty
        exist_tf.point = tf.point
        exist_tf.question = tf.question
        exist_tf.corr_answer = tf.corr_answer
        db.session.commit()
        return tf

    
    # delete question
    def delete_mcq(self, id):
        if type(id) == str:
            id = int(id)
        mcq = db.session.get(Mcq, id)    
        if mcq:
            db.session.delete(mcq)
            db.session.commit()
            return True
        else:
            return False  
    def delete_tf(self, id):
        if type(id) == str:
            id = int(id)
        tf = db.session.get(Tf, id)    
        if tf:
            db.session.delete(tf)
            db.session.commit()
            return True
        else:
            return False           