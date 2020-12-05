from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired

from app.models import Conference, Team

def validate_unique_field(field, original, table, field_name):
    if (original is None) or (field.data != original):
        entry = table.query.filter_by(**{field_name: field.data}).first()
        if entry is not None:
            raise ValidationError(f'Please use a different value for {field_name}.')

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
        validate_unique_field(name, self.original_name, Conference, 'name')

    def validate_nickname(self, nickname):
        validate_unique_field(nickname, self.original_nickname, Conference, 'nickname')


def AddConferenceForm():
    return AddOrEditConferenceForm()

def EditConferenceForm(conference):
    return AddOrEditConferenceForm(original_conference=conference)

class AddOrEditTeamForm(FlaskForm):
    school = StringField('School Name', validators=[DataRequired()])
    mascot = StringField('Mascot', validators=[DataRequired()])
    abbr = StringField('Abbreviation', validators=[DataRequired()])
    logo = StringField('Logo URL')
    conference_id = SelectField('Conference', validators=[DataRequired()], coerce=int)
    about = TextAreaField('About')
    submit = SubmitField('Submit')

    def __init__(self, original_team=None, *args, **kwargs):
        super(AddOrEditTeamForm, self).__init__(*args, **kwargs)
        conf_choices = [(c.id, c.nickname) for c in Conference.query.all()]
        self.conference_id.choices = conf_choices
        self.original_school = None
        self.original_mascot = None
        self.original_abbr = None
        if original_team:
            self.original_school = original_team.school
            self.original_mascot = original_team.mascot
            self.original_abbr = original_team.abbr

    def validate_school(self, school):
        validate_unique_field(school, self.original_school, Team, 'school')

    def validate_abbr(self, abbr):
        validate_unique_field(abbr, self.original_abbr, Team, 'abbr')

# class Team(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     school = db.Column(db.String)
#     mascot = db.Column(db.String)
#     abbr = db.Column(db.String)
#     about = db.Column(db.String)
#     logo = db.Column(db.String)
#     conference_id = db.Column(db.Integer, db.ForeignKey('conference.id'))
