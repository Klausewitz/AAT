from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, TextAreaField, BooleanField, widgets
from wtforms.validators import DataRequired
from wtforms_alchemy import QuerySelectMultipleField


class McqForm(FlaskForm):

    tag = StringField(label='tag', validators=[DataRequired()])
    difficulty = StringField(label='difficulty', validators=[DataRequired()])
    point = StringField(label='point', validators=[DataRequired()])
    question = StringField(label='question', validators=[DataRequired()])
    option1 = StringField(label='option1', validators=[DataRequired()])
    option2 = StringField(label='option2', validators=[DataRequired()])
    option3 = StringField(label='option3', validators=[DataRequired()])
    option4 = StringField(label='option4', validators=[DataRequired()])
    option5 = StringField(label='option5', validators=[DataRequired()])
    corr_answer = StringField(label='correct answer', validators=[DataRequired()])
    submit = SubmitField(label='submit')
  

class TfForm(FlaskForm):

    tag = StringField(label='tag')
    difficulty = StringField(label='difficulty')
    point = StringField(label='point', validators=[DataRequired()])
    question = TextAreaField(label='question', validators=[DataRequired()])
    corr_answer = StringField(label='correct answer ("false", "0" for false, "ture", "1" for true)', validators=[DataRequired()])
    submit = SubmitField(label='submit')
  

class DeleteQuestionForm(FlaskForm):

    id = HiddenField(validators=[DataRequired()])
    submit = SubmitField(label='Confirm')  

################################# assignment question ###########################################

# supportive function
class QuerySelectMultipleFieldWithCheckboxes(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AssignmentQuestionForm(FlaskForm):
    choices = QuerySelectMultipleFieldWithCheckboxes("Choices")
    submit = SubmitField(label='Confirm')


class DeleteAssignmentQuestionForm(FlaskForm):

    id = HiddenField(validators=[DataRequired()])
    submit = SubmitField(label='Confirm')    