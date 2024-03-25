from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, ValidationError
from wtforms.validators import DataRequired, AnyOf, URL, Regexp
from enums import Gender

class MovieForm(FlaskForm):
    
    name = StringField(
        'name', validators=[DataRequired()]
    )

    release_date = DateTimeField(
        'release_date',
        validators=[DataRequired()],
        default= datetime.today()
    )


class ActorForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    age = StringField(
        'age', validators=[DataRequired()]
    )
    gender = SelectField(
        'gender', validators=[DataRequired()],
        choices=Gender.choices()
    )
