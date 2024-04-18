from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user
from forms.assignment_form import AssignmentForm, DeleteAssignmentForm
from forms.question_form import AssignmentQuestionForm, McqForm, DeleteQuestionForm, DeleteAssignmentQuestionForm, TfForm
from models.models import Assignment, AssignmentService, Mcq, ModuleService, QuestionService, Tf, UserService
from routes import app


@app.route('/dashboard')
@login_required
def dashboard():
    modules = current_user.modules
    return render_template('dashboard.html', modules=modules)


@app.route('/module/<module_id>', methods=['GET', 'POST'])
@login_required
def module(module_id):
    if current_user.is_staff == 1:
        # render del form
        delete_assignment_form = DeleteAssignmentForm()
        if delete_assignment_form.validate_on_submit():
            # print(int(delete_assignment_form.assignment_id.data))
            del_result = AssignmentService().delete_assignment(int(delete_assignment_form.assignment_id.data))
            if del_result:
                flash('Assignment successfully deleted', category='success')
            else:
                flash('Failed on deleting the assignment', category='warning')
    module = ModuleService().get_module(module_id)
    assignments = AssignmentService().get_module_assignment(module)
    if current_user.is_staff == 1:
        return render_template('module.html', module=module, assignments=assignments, delete_assignment_form=delete_assignment_form)
    else:
        return render_template('module.html', module=module, assignments=assignments)


@app.route('/module/<module_id>/new_assignment', methods=['GET', 'POST'])
@login_required
def new_assignment(module_id):
    if current_user.is_staff != 1:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        form = AssignmentForm()
        if form.validate_on_submit():
            new_assignment = Assignment()
            new_assignment.name = form.name.data            
            new_assignment.module_id = int(module_id) 
            new_assignment.is_open = int(form.is_open.data)   
            new_assignment.max_attempts = int(form.max_attempts.data)     
            try:
                AssignmentService().new_assignment(new_assignment)
                flash('Assignment successfully created', category='success')
                return redirect(url_for('module', module_id=module_id))
            except:
                flash('Assignment create failed', category='danger')  
        return render_template('edit_assignment.html', form=form, edit=False, module_id=module_id)
    

@app.route('/module/<module_id>/edit_assignment/<assignment_id>', methods=['GET', 'POST'])
@login_required
def edit_assignment(module_id, assignment_id):
    if current_user.is_staff != 1:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        form = AssignmentForm()
        if request.method == 'GET':
            try:
                assignment = AssignmentService().get_assignment(int(assignment_id))
                if not assignment:
                    flash('No such an assignment in database', category='warning')
                    return redirect(url_for('module', module_id=module_id))
                else:
                    form.name.data = assignment.name
                    form.is_open.data = assignment.is_open
                    form.max_attempts.data = assignment.max_attempts
            except:
                flash('Failed on getting the assignment', category='danger')   
                return redirect(url_for('module', module_id=module_id))
        # after click on submit btn    
        if form.validate_on_submit():
            edited_assignment = Assignment()
            edited_assignment.id = int(assignment_id)
            edited_assignment.name = form.name.data
            edited_assignment.module_id = int(module_id)
            edited_assignment.is_open = int(form.is_open.data)
            edited_assignment.max_attempts = int(form.max_attempts.data)
            try:
                AssignmentService().edit_assignment(edited_assignment)
                flash('Assignment successfully updated', category='success')
                return redirect(url_for('module', module_id=module_id))
            except:
                flash('Assignment update failed', category='danger')
        else:
            print(f'not submit? {form.is_submitted()}. not validated? {form.validate()}')        
        return render_template('edit_assignment.html', form=form, edit=True, module_id=module_id) 
    

@app.route('/module/<module_id>/assignment/<assignment_id>', methods=['GET', 'POST'])
@login_required
def assignment(module_id, assignment_id):
    module = ModuleService().get_module(module_id)
    assignment = AssignmentService().get_assignment(assignment_id)
    mcqs = AssignmentService().get_all_current_mcqs(assignment) 
    tfs = AssignmentService().get_all_current_tfs(assignment) 
    return render_template('assignment.html', module=module, assignment=assignment, mcqs=mcqs, tfs=tfs)

################################## question bank ####################################

@app.route('/module/<module_id>/question_bank/choose', methods=['GET', 'POST'])
@login_required
def question_bank_choose(module_id):
    if current_user.is_staff == 0:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        module = ModuleService().get_module(module_id)
        return render_template('question/question_choose.html', module=module)


@app.route('/module/<module_id>/question_bank/mcq', methods=['GET', 'POST'])
@login_required
def mcq_question_bank(module_id):
    if current_user.is_staff == 0:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        if current_user.is_staff == 1:
            # render del form
            delete_question_form = DeleteQuestionForm()
            if delete_question_form.validate_on_submit():
                del_result = QuestionService().delete_mcq(int(delete_question_form.id.data))
                if del_result:
                    flash('Question successfully deleted', category='success')
                else:
                    flash('Failed on deleting the question', category='waring')
        module = ModuleService().get_module(module_id)
        questions = QuestionService().get_all_mcqs()
        if current_user.is_staff == 1:
            return render_template('question/all_mcq_list.html', module=module, questions=questions, delete_question_form=delete_question_form)
        else:
            return render_template('question/all_mcq_list.html', module=module, questions=questions)


@app.route('/module/<module_id>/question_bank/tf', methods=['GET', 'POST'])
@login_required
def tf_question_bank(module_id):
    if current_user.is_staff == 0:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        if current_user.is_staff == 1:
            # render del form
            delete_question_form = DeleteQuestionForm()
            if delete_question_form.validate_on_submit():
                del_result = QuestionService().delete_tf(int(delete_question_form.id.data))
                if del_result:
                    flash('Question successfully deleted', category='success')
                else:
                    flash('Failed on deleting the question', category='waring')
        module = ModuleService().get_module(module_id)
        questions = QuestionService().get_all_tfs()
        if current_user.is_staff == 1:
            return render_template('question/all_tf_list.html', module=module, questions=questions, delete_question_form=delete_question_form)
        else:
            return render_template('question/all_tf_list.html', module=module, questions=questions)
    

@app.route('/module/<module_id>/question_bank/mcq/new', methods=['GET', 'POST'])
@login_required
def new_mcq(module_id):
    if current_user.is_staff != 1:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        form = McqForm()
        if form.validate_on_submit():
            new_mcq = Mcq() 
            new_mcq.module_id = int(module_id) 
            new_mcq.tag = form.tag.data 
            new_mcq.difficulty = int(form.difficulty.data)
            new_mcq.point = int(form.point.data)
            new_mcq.question = form.question.data 
            new_mcq.option1 = form.option1.data 
            new_mcq.option2 = form.option2.data 
            new_mcq.option3 = form.option3.data 
            new_mcq.option4 = form.option4.data 
            new_mcq.option5 = form.option5.data 
            new_mcq.corr_answer = form.corr_answer.data 
            try:
                QuestionService().new_mcq(new_mcq)
                flash('Question successfully uploaded', category='success')
                return redirect(url_for('mcq_question_bank', module_id=module_id))
            except:
                flash('Question upload failed', category='danger')  
        return render_template('question/edit_mcq.html', form=form, edit=False, module_id=module_id)    
    

@app.route('/module/<module_id>/question_bank/tf/new', methods=['GET', 'POST'])
@login_required
def edited_tf(module_id):
    if current_user.is_staff != 1:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        form = TfForm()
        if form.validate_on_submit():
            new_tf = Tf() 
            new_tf.module_id = int(module_id) 
            new_tf.tag = form.tag.data 
            try:
                new_tf.difficulty = int(form.difficulty.data)
            except:
                new_tf.difficulty = form.difficulty.data  
            new_tf.point = int(form.point.data)
            new_tf.question = form.question.data 
            if form.corr_answer.data == 1 or form.corr_answer.data == 'true' or form.corr_answer.data == True:
                new_tf.corr_answer = 1
            elif form.corr_answer.data == 0 or form.corr_answer.data == 'false' or form.corr_answer.data == False:
                new_tf.corr_answer = 0
            else:      
                new_tf.corr_answer = form.corr_answer.data 
            try:
                QuestionService().new_tf(new_tf)
                flash('Question successfully uploaded', category='success')
                return redirect(url_for('tf_question_bank', module_id=module_id))
            except:
                flash('Question upload failed', category='danger')  
        return render_template('question/edit_tf.html', form=form, edit=False, module_id=module_id)      


@app.route('/module/<module_id>/question_bank/mcq/<mcq_id>', methods=['GET', 'POST'])
@login_required
def edit_mcq(module_id, mcq_id):
    if current_user.is_staff != 1:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        form = McqForm()
        if request.method == 'GET':
            try:
                mcq = QuestionService().get_mcq(int(mcq_id))
                if not mcq:
                    flash('No such a question in database', category='warning')
                    return redirect(url_for('mcq_question_bank', module_id=module_id))
                else:
                    form.tag.data = mcq.tag
                    form.difficulty.data = mcq.difficulty
                    form.point.data = mcq.point
                    form.question.data = mcq.question
                    form.option1.data = mcq.option1
                    form.option2.data = mcq.option2
                    form.option3.data = mcq.option3
                    form.option4.data = mcq.option4
                    form.option5.data = mcq.option5
                    form.corr_answer.data = mcq.corr_answer
            except:
                flash('Failed on getting the assignment', category='danger')   
                return redirect(url_for('module', module_id=module_id))
        # after click on submit btn    
        if form.validate_on_submit():
            edited_mcq = Mcq()
            edited_mcq.id = int(mcq_id)
            edited_mcq.module_id = int(module_id) 
            edited_mcq.tag = form.tag.data 
            edited_mcq.difficulty = int(form.difficulty.data)
            edited_mcq.point = int(form.point.data)
            edited_mcq.question = form.question.data 
            edited_mcq.option1 = form.option1.data 
            edited_mcq.option2 = form.option2.data 
            edited_mcq.option3 = form.option3.data 
            edited_mcq.option4 = form.option4.data 
            edited_mcq.option5 = form.option5.data 
            edited_mcq.corr_answer = form.corr_answer.data 
            try:
                QuestionService().edit_mcq(edited_mcq)
                flash('Question successfully updated', category='success')
                return redirect(url_for('mcq_question_bank', module_id=module_id))
            except:
                flash('Question update failed', category='danger')
        else:
            print(f'not submit? {form.is_submitted()}. not validated? {form.validate()}')        
        return render_template('question/edit_mcq.html', form=form, edit=True, module_id=module_id) 
    

@app.route('/module/<module_id>/question_bank/tf/<tf_id>', methods=['GET', 'POST'])
@login_required
def edit_tf(module_id, tf_id):
    if current_user.is_staff != 1:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        form = TfForm()
        if request.method == 'GET':
            try:
                tf = QuestionService().get_tf(int(tf_id))
                if not tf:
                    flash('No such a question in database', category='warning')
                    return redirect(url_for('tf_question_bank', module_id=module_id))
                else:
                    form.tag.data = tf.tag
                    form.difficulty.data = tf.difficulty
                    form.point.data = tf.point
                    form.question.data = tf.question
                    if tf.corr_answer == 0:
                        form.corr_answer.data = 'false'
                    elif tf.corr_answer == 1:
                        form.corr_answer.data = 'true'
                    else:
                        form.corr_answer.data = tf.corr_answer
            except:
                flash('Failed on getting the assignment', category='danger')   
                return redirect(url_for('module', module_id=module_id))
        # after click on submit btn    
        if form.validate_on_submit():
            edited_tf = Tf()
            edited_tf.id = int(tf_id)
            edited_tf.module_id = int(module_id) 
            edited_tf.tag = form.tag.data 
            try:
                edited_tf.difficulty = int(form.difficulty.data)
            except:
                edited_tf.difficulty = form.difficulty.data
            edited_tf.point = int(form.point.data)
            edited_tf.question = form.question.data 
            if form.corr_answer.data == 1 or form.corr_answer.data == 'true' or form.corr_answer.data == True:
                edited_tf.corr_answer = 1
            elif form.corr_answer.data == 0 or form.corr_answer.data == 'false' or form.corr_answer.data == False:
                edited_tf.corr_answer = 0
            else:      
                edited_tf.corr_answer = form.corr_answer.data 
            try:
                QuestionService().edit_tf(edited_tf)
                flash('Question successfully updated', category='success')
                return redirect(url_for('tf_question_bank', module_id=module_id))
            except:
                flash('Question update failed', category='danger')
        else:
            print(f'not submit? {form.is_submitted()}. not validated? {form.validate()}')        
        return render_template('question/edit_tf.html', form=form, edit=True, module_id=module_id)     
    
############################ question assign ######################################

@app.route('/module/<module_id>/assign_question/<assignment_id>', methods=['GET', 'POST'])
@login_required
def assign_question_choose(module_id, assignment_id):    
    if current_user.is_staff != 1:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        module = ModuleService().get_module(module_id)
        assignment = AssignmentService().get_assignment(assignment_id)
        return render_template('question/assignment_question/assign_question_choose.html', module=module, assignment=assignment)
    

@app.route('/module/<module_id>/assign_question/question/<question_type>', methods=['GET', 'POST'])
@login_required  
def question_choose_assignment(module_id, question_type): 
    if current_user.is_staff != 1:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        module = ModuleService().get_module(module_id)
        assignments = AssignmentService().get_module_assignment(module=module)
        return render_template('question/assignment_question/question_choose_assignment.html', module=module, assignments=assignments, question_type=question_type)


@app.route('/module/<module_id>/assign_question/<question_type>/<assignment_id>', methods=['GET', 'POST'])
@login_required 
def assignment_all_question(module_id, question_type, assignment_id):
    if current_user.is_staff != 1:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        # render del form
        delete_assignment_question_form = DeleteAssignmentQuestionForm()
        assignment = AssignmentService().get_assignment(id=int(assignment_id))
        if delete_assignment_question_form.validate_on_submit():
            if question_type == 'mcq':
                question = QuestionService().get_mcq(int(delete_assignment_question_form.id.data))
                del_result = AssignmentService().delete_assignment_mcq(assignment=assignment, mcq=question)   
            elif question_type == 'tf':
                question = QuestionService().get_tf(int(delete_assignment_question_form.id.data))
                del_result = AssignmentService().delete_assignment_tf(assignment=assignment, tf=question)   
            else:
                flash('Please check question type in url', category='danger')    
            if del_result:
                flash('Question successfully removed', category='success')
            else:
                flash('Failed on removing question', category='danger')
        module = ModuleService().get_module(module_id)        
        # load questions        
        if question_type == 'mcq':
            questions = AssignmentService().get_all_current_mcqs(assignment=assignment) 
        elif question_type == 'tf':
            questions = AssignmentService().get_all_current_tfs(assignment=assignment)   
        else:
            flash('Please check question type in url', category='danger') 
        return render_template('question/assignment_question/assignment_question.html', module=module, question_type=question_type, assignment=assignment, questions=questions, delete_assignment_question_form=delete_assignment_question_form)


@app.route('/module/<module_id>/assign_question/<question_type>/<assignment_id>/new', methods=['GET', 'POST'])
@login_required 
def new_assignment_question(module_id, question_type, assignment_id): 
    assignment_id = int(assignment_id)
    assignment = AssignmentService().get_assignment(assignment_id)
    module = ModuleService().get_module(int(module_id))
    if current_user.is_staff != 1:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        if question_type == 'mcq':
            choices = AssignmentService().get_assignment_other_mcqs(assignment_id)
            current_questions = AssignmentService().get_all_current_mcqs(assignment) 
        elif question_type == 'tf':
            choices = AssignmentService().get_assignment_other_tfs(assignment_id)  
            current_questions = AssignmentService().get_all_current_tfs(assignment) 
        else:
            flash('Please check question type in url', category='danger') 
        form = AssignmentQuestionForm(data={"choices": current_questions})
        form.choices.query = choices
        if form.validate_on_submit():
            if question_type == 'mcq':
                result = AssignmentService().new_assignment_mcqs(assignment, form.choices.data)
            elif question_type == 'tf':
                result = AssignmentService().new_assignment_tfs(assignment, form.choices.data)
            else:
                flash('Please check question type in url', category='danger') 
            if result:
                flash('Question successfully added', category='success')
                return redirect(url_for('module', module_id=module_id))
            else:
                flash('Failed on adding question', category='waring')
        return render_template('question/assignment_question/new_assignment_question.html', question_type=question_type, module=module, assignment=assignment, form=form)