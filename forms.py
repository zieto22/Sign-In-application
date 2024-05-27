# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class TodoForm(FlaskForm):
    """
    A form class for creating a todo item.

    Attributes:
        description (StringField): The description of the todo item.
        submit (SubmitField): The submit button for adding the todo item.
    """
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Todo')
