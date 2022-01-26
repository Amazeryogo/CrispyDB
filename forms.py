from flask_wtf import FlaskForm as Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, PasswordField
from wtforms import validators, ValidationError



class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    submit = SubmitField('Login')


class NewCollectionForm(Form):
    name = TextField('Add a new Collection')
    submit = SubmitField('Create')


