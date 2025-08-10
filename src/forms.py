from flask_wtf import FlaskForm
import wtforms


class LoginForm(FlaskForm):
    username = wtforms.StringField('Username', validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField('Password', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Login')


class NewCollectionForm(FlaskForm):
    name = wtforms.StringField('Make A New Collection', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Create')


class Changeauth(FlaskForm):
    old_password = wtforms.PasswordField('Old Password', validators=[wtforms.validators.DataRequired()])
    new_password = wtforms.PasswordField('New Password', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Change')


def create_edit_form(doc):
    class EditForm(FlaskForm):
        pass

    for key, value in doc.items():
        if key == '_id':
            field = wtforms.StringField(key, default=value, render_kw={'readonly': True})
        else:
            field = wtforms.StringField(key, default=value)
        setattr(EditForm, key, field)

    EditForm.submit = wtforms.SubmitField('Update')
    return EditForm()
