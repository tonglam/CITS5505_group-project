"""
Forms for handling community creation or edition related inputs.
This module defines Flask-WTF forms for creating and updating communities.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired


class CommunityForm(FlaskForm):
    """
    Form for creating or editing a new community.
    Includes fields for community avatar, name, description, and category ID.
    """

    avatar = FileField(
        "avatar", validators=[FileAllowed(["jpg", "jpeg", "png"], "Images only!")]
    )
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description", validators=[DataRequired()])
    category_select = SelectField(
        "Select Option", validators=[DataRequired()], choices=[]
    )
    creator_id = StringField("creator_id")
