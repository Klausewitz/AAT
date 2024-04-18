from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class ModuleForm(FlaskForm):

    name = StringField(label='name', validators=[DataRequired()])
    code = StringField(label='code', validators=[DataRequired()])
    submit = SubmitField(label='submit')
  

class DeleteModuleForm(FlaskForm):

    module_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField(label='Confirm')
