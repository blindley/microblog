from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length

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
        if (self.original_name is not None) and (name.data != self.original_name):
            conference = Conference.query.filter_by(name=name.data).first()
            if conference is not None:
                raise ValidationError('Please use a different conference name.')

    def validate_nickname(self, nickname):
        if (self.original_nickname is not None) and (nickname.data != self.original_nickname):
            conference = Conference.query.filter_by(nickname=nickname.data).first()
            if conference is not None:
                raise ValidationError('Please use a different conference nickname.')

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

