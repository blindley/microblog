from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length

from app.models import Conference

class AddConferenceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired()])
    hq = StringField('Headquarters')
    logo = StringField('Logo URL')
    about = TextAreaField('About')
    submit = SubmitField('Submit')

    def validate_name(self, name):
        conference = Conference.query.filter_by(name=name.data).first()
        if conference is not None:
            raise ValidationError('Please use a different conference name.')

    def validate_nickname(self, nickname):
        conference = Conference.query.filter_by(nickname=nickname.data).first()
        if conference is not None:
            raise ValidationError('Please use a different conference nickname.')

