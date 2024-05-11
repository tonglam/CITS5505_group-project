from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import (DataRequired)

class CreateForm(FlaskForm):

    name = StringField(
        "name",validators=[DataRequired()]
    )
    description = StringField(
        "description",validators=[DataRequired()]
    )
    category_id = StringField(
        "category_id",validators=[DataRequired()]
    )

