from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired

from app.models import Conference

class AddOrEditConferenceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired()])
    hq = StringField('Headquarters')
    logo = StringField('Logo URL')
    about = TextAreaField('About')
    submit = SubmitField('Submit')

    def __init__(self, original_conference=None, *args, **kwargs):
        super(AddOrEditConferenceForm, self).__init__(*args, **kwargs)
        self.original_name = None
        self.original_nickname = None
        if original_conference:
            self.original_name = original_conference.name
            self.original_nickname = original_conference.nickname

    def validate_name(self, name):
        if (self.original_name is None) or (name.data != self.original_name):
            conference = Conference.query.filter_by(name=name.data).first()
            if conference is not None:
                raise ValidationError('Please use a different conference name.')

    def validate_nickname(self, nickname):
        if (self.original_nickname is None) or (nickname.data != self.original_nickname):
            conference = Conference.query.filter_by(nickname=nickname.data).first()
            if conference is not None:
                raise ValidationError('Please use a different conference nickname.')

def AddConferenceForm():
    return AddOrEditConferenceForm()

def EditConferenceForm(conference):
    return AddOrEditConferenceForm(original_conference=conference)
