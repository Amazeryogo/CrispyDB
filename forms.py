from flask_wtf import FlaskForm
import wtforms


class LoginForm(FlaskForm):
    username = wtforms.StringField('Username', validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField('Password', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Login')


class NewCollectionForm(FlaskForm):
    name = wtforms.StringField('Name', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Create')

class Changeauth(FlaskForm):
    old_password = wtforms.PasswordField('Old Password', validators=[wtforms.validators.DataRequired()])
    new_password = wtforms.PasswordField('New Password', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Change')