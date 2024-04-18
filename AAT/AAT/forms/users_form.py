from flask_wtf import FlaskForm
from wtforms import Field, SelectMultipleField, StringField, PasswordField, SubmitField, HiddenField, widgets
from wtforms.validators import DataRequired
from wtforms_alchemy import QuerySelectMultipleField


'''
validators=[DataRequired(message='xx cannot be empty'), 
Length(min=6,max=30,message='length between 6 - 30')
Email(message='Please check you email address')]
'''
       

# forms
class LoginForm(FlaskForm):
    
    username = StringField(label='username:', validators=[DataRequired()])
    password = PasswordField(label='password:', validators=[DataRequired()])
    submit   = SubmitField(label='login')


class UserForm(FlaskForm):

    username = StringField(label='username:', validators=[DataRequired()])
    password = PasswordField(label='password:', validators=[DataRequired()])
    is_staff = StringField(label='is he / she a staff?', validators=[DataRequired()])
    year     = StringField(label='year:', validators=[DataRequired()])
    submit   = SubmitField(label='submit')


class EditUserForm(FlaskForm):

    is_staff = StringField(label='is_staff:', validators=[DataRequired()])
    year     = StringField(label='year:', validators=[DataRequired()])
    submit   = SubmitField(label='submit')    


class ChangePswForm(FlaskForm):
    
    old_password = PasswordField(label='Old password:', validators=[DataRequired()])
    password     = PasswordField(label='New password:', validators=[DataRequired()])
    cfm_password = PasswordField(label='Confirm password:', validators=[DataRequired()])
    submit       = SubmitField(label='submit')
  

class DeleteUserForm(FlaskForm):

    user_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField(label='Confirm')


class QuerySelectMultipleFieldWithCheckboxes(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class UserModuleForm(FlaskForm):
    choices = QuerySelectMultipleFieldWithCheckboxes("Choices")
    submit = SubmitField(label='Confirm')


class DeleteUserModuleForm(FlaskForm):

    module_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField(label='Confirm')



########################################################################################

'''
# supportive class
class MultiCheckboxField(Field):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

    def __init__(self, label='', validators=None, choices=[], **kwargs):
        super().__init__(label, validators, **kwargs)
        self.choices = choices

    def process_formdata(self, valuelist):
        self.data = [choice for choice in self.choices if choice[0] in valuelist]

    def pre_validate(self, form):
        if self.data:
            known_choices = [choice[0] for choice in self.choices]
            for d in self.data:
                if d not in known_choices:
                    raise ValueError(self.gettext('Not a valid choice'))
                

class UserModuleForm_1(FlaskForm):

    def __init__(self, choices=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = MultiCheckboxField(label='Select Modules', choices=choices)
        self.submit = SubmitField(label='Confirm')
'''    