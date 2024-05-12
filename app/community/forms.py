"""
Forms for handling community creation related inputs.
This module defines Flask-WTF forms for creating and updating communities.
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import (DataRequired)

class CreateForm(FlaskForm):
    """
    Form for creating a new community.
    Includes fields for community name, description, and category ID.
    """
    name = StringField(
        "name",validators=[DataRequired()]
    )
    description = StringField(
        "description",validators=[DataRequired()]
    )
    category_id = StringField(
        "category_id",validators=[DataRequired()]
    )