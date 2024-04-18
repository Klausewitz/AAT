import bcrypt
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from forms.users_form import DeleteUserForm, DeleteUserModuleForm, EditUserForm, UserForm, UserModuleForm
from forms.modules_form import DeleteModuleForm, ModuleForm
from models.models import Module, ModuleService, User, UserService
from routes import app


######################################## user #########################################

# add new user into database
@app.route('/dashboard/new_user', methods=['GET', 'POST'])
@login_required
def new_user():    
    if current_user.is_staff != 2:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        form = UserForm()
        print(form.validate())
        if form.validate_on_submit():
            new_user = User()
            new_user.username = form.username.data            
            hsd_psw = bcrypt.hashpw(form.password.data.encode(), bcrypt.gensalt())
            new_user.password = hsd_psw.decode('utf-8')
            try:
                new_user.is_staff = int(form.is_staff.data)
            except:
                flash('please check your input on "is staff" part', category='danger')   
            try:
                new_user.year = int(form.year.data)
            except:
                flash('please check your input on "year" part', category='danger')   
            try:
                UserService().new_user(new_user)
                flash('User successfully created', category='success')
                return redirect(url_for('dashboard'))
            except:
                flash('User create failed', category='danger')  
        return render_template('admin/edit_user.html', form=form, edit=False)


# all user list
@app.route('/dashboard/edit_user/all_users', methods=['GET', 'POST'])
@login_required   
def edit_all_users(): 
    if current_user.is_staff != 2:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        # render del user form
        delete_user_form = DeleteUserForm()
        if delete_user_form.validate_on_submit():
            del_result = UserService().delete_user(int(delete_user_form.user_id.data))
            if del_result:
                flash('User successfully deleted', category='success')
            else:
                flash('Failed on deleting the user', category='waring')
        # load user form            
        users = UserService().get_all_users()
        return render_template('admin/all_user_list.html', users=users, delete=True, delete_user_form=delete_user_form, permission=False)


# edit user information
@app.route('/dashboard/edit_user/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_user_information(user_id):
    if current_user.is_staff != 2:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        form = EditUserForm()  
        if request.method == 'GET':
            try:
                user = UserService().get_user(int(user_id))
                if not user:
                    flash('No such an user in database', category='warning')
                    return redirect(url_for('edit_all_users'))
                else:
                    form.is_staff.data = user.is_staff
                    form.year.data = user.year
            except:
                flash('Failed on getting the user', category='danger')   
                return redirect(url_for('edit_all_users'))  
        if form.validate_on_submit():
            user = UserService().get_user(int(user_id))
            try:
                user.is_staff = int(form.is_staff.data)
            except:
                flash('please check your input on "is staff" part', category='danger')   
            try:
                user.year = int(form.year.data)
            except:
                flash('please check your input on "year" part', category='danger')    
            try:
                UserService().edit_user(user, form.is_staff.data, form.year.data)
                flash('User successfully edited', category='success')
                return redirect(url_for('dashboard'))
            except:
                flash('User edit failed', category='danger')          
    return render_template('admin/edit_user.html', form=form, edit=True)


###################################### module #########################################


# add new module into database
@app.route('/dashboard/new_module', methods=['GET', 'POST'])
@login_required
def new_module():    
    if current_user.is_staff != 2:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        form = ModuleForm()
        print(form.validate())
        if form.validate_on_submit():
            new_module = Module()
            new_module.name = form.name.data            
            new_module.code = form.code.data   
            try:
                ModuleService().new_module(new_module)
                flash('Module successfully created', category='success')
                return redirect(url_for('dashboard'))
            except:
                flash('Module create failed', category='danger')  
        return render_template('admin/edit_module.html', form=form, edit=False)


# all module list
@app.route('/dashboard/edit_module/all_modules', methods=['GET', 'POST'])
@login_required   
def edit_all_modules(): 
    if current_user.is_staff != 2:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        # render del module form
        delete_module_form = DeleteModuleForm()
        if delete_module_form.validate_on_submit():
            del_result = ModuleService().delete_module(int(delete_module_form.module_id.data))
            if del_result:
                flash('Module successfully deleted', category='success')
            else:
                flash('Failed on deleting the module', category='danger')
        # load module form            
        modules = ModuleService().get_all_modules()
        return render_template('admin/all_module_list.html', modules=modules, delete=True, delete_module_form=delete_module_form)


# edit module information
@app.route('/dashboard/edit_module/<module_id>', methods=['GET', 'POST'])
@login_required
def edit_module_information(module_id): 
    if current_user.is_staff != 2:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        form = ModuleForm()
        if request.method == 'GET':
            try:
                module = ModuleService().get_module(int(module_id))
                if not module:
                    flash('No such a module in database', category='warning')
                    return redirect(url_for('edit_all_modules'))
                else:
                    form.name.data = module.name
                    form.code.data = module.code
            except:
                flash('Failed on getting the module', category='danger')   
                return redirect(url_for('edit_all_modules'))
        # after click on submit btn    
        if form.validate_on_submit():
            edited_module = Module()
            edited_module.id = int(module_id)
            edited_module.name = form.name.data
            edited_module.code = form.code.data
            try:
                ModuleService().edit_module(edited_module)
                flash('module successfully updated', category='success')
                return redirect(url_for('edit_all_modules'))
            except:
                flash('Module update failed', category='danger')
        return render_template('admin/edit_module.html', form=form, edit=True)


################################## user_module #####################################


# all user list
@app.route('/dashboard/edit_permission/all_users', methods=['GET', 'POST'])
@login_required   
def edit_permission_all_users(): 
    if current_user.is_staff != 2:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        # load user form            
        users = UserService().get_all_users()
        return render_template('admin/all_user_list.html', users=users, delete=False, permission=True)


# all current permission
@app.route('/dashboard/edit_permission/<user_id>', methods=['GET', 'POST'])
@login_required   
def edit_user_permission(user_id): 
    user_id = int(user_id)
    if current_user.is_staff != 2:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        # render del module form
        delete_user_module_form = DeleteUserModuleForm()
        user = UserService().get_user(id=user_id)
        if delete_user_module_form.validate_on_submit():
            module = ModuleService().get_module(int(delete_user_module_form.module_id.data))
            del_result = UserService().delete_user_module(user, module)
            if del_result:
                flash('User module permission successfully removed', category='success')
            else:
                flash('Failed on removing user module permission', category='waring')
        # load module form            
        modules = UserService().get_all_current_modules(user_id)
        return render_template('admin/user_module/user_module.html', user=user, modules=modules, delete=True, delete_user_module_form=delete_user_module_form)


# add new permission
@app.route('/dashboard/edit_permission/<user_id>/add', methods=['GET', 'POST'])
@login_required   
def add_user_module(user_id): 
    user_id = int(user_id)
    user = UserService().get_user(id=user_id)
    if current_user.is_staff != 2:
        flash('Sorry, you do not have the permission', category='danger')
        return redirect(url_for('dashboard'))
    else:
        # all_modules = ModuleService().get_all_modules()
        choices = UserService().get_user_other_modules(user_id)
        current_modules = UserService().get_all_current_modules(user_id)
        form = UserModuleForm(data={"choices": current_modules})
        form.choices.query = choices
        if form.validate_on_submit():
            result = UserService().new_user_modules(user, form.choices.data)
            if result:
                flash('User module permission successfully added', category='success')
                return redirect(url_for('edit_user_permission', user_id=user_id))
            else:
                flash('Failed on adding user module permission', category='waring')

        return render_template('admin/user_module/new_user_module.html', user=user, form=form)
