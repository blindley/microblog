from flask import request
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    comment = TextAreaField('Say something', validators=[DataRequired()])
    submit = SubmitField('Submit')

