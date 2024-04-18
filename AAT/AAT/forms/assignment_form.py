from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, IntegerField
from wtforms.validators import DataRequired


class AssignmentForm(FlaskForm):

    name = StringField(label='name', validators=[DataRequired()])
    is_open = StringField(label='is assignment open?', validators=[DataRequired()])
    max_attempts = StringField(label='maximum attempts', validators=[DataRequired()])
    submit = SubmitField(label='submit')
  

class DeleteAssignmentForm(FlaskForm):

    assignment_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField(label='Confirm')
