from flask_wtf import FlaskForm
import wtforms


class LoginForm(FlaskForm):
    username = wtforms.StringField('Username', validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField('Password', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Login')


class NewCollectionForm(FlaskForm):
    name = wtforms.StringField('Name', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Create')

class CliOnWebUI(FlaskForm):
    command = wtforms.StringField('Command', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Submit')