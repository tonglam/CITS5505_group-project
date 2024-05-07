from flask_wtf import FlaskForm
from wtforms import StringField

class CreateForm(FlaskForm):

    name = StringField(
        "name"
    )
    description = StringField(
        "description"
    )
    category_id = StringField(
        "category_id"
    )

