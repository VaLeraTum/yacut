from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, URL


class URLForm(FlaskForm):
    original_link = URLField(validators=[DataRequired(), URL(), Length(max=2048)])
    custom_id = StringField(validators=[Length(max=16)])
    submit = SubmitField('Создать')
