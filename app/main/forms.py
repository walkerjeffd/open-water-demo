from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import User, Location, Project


class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class UploadDatasetForm(Form):
    location = SelectField('Location', coerce=int)
    project = SelectField('Project', coerce=int)
    file = FileField('File', validators=[FileRequired(), FileAllowed(['csv', 'CSV files only'])])
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(UploadDatasetForm, self).__init__(*args, **kwargs)
        self.location.choices = [(location.id, location.name)
                             for location in Location.query.order_by(Location.name).all()]
        self.project.choices = [(project.id, project.name)
                             for project in Project.query.order_by(Project.name).all()]
        self.user = user