from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, PasswordField
from wtforms import validators, ValidationError

Form = FlaskForm


class LoginForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')


class NewCollectionForm(Form):
    name = TextField('Add a new Collection')
    submit = SubmitField('Create')


class DeleteCollectionForm(Form):
    submit = SubmitField('Delete')


class AddDataForm(Form):
    data = TextAreaField('data')
    submit = SubmitField('Add')
