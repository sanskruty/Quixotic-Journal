from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired,Length,Email,EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Enter your name"), Length(min=2,max=25)])
    email = EmailField('Email', validators=[DataRequired("Email required"), Email("The email format should be proper")])
    password = PasswordField('Password', validators=[DataRequired()])
    type = SelectField('Type', validators=[DataRequired()], choices=[("poet", "Poet"), ("reader", "Reader")])
    # confirmPassword = PasswordField('Repeat Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email("The email format should be proper")])
    password = PasswordField('Password', validators=[DataRequired()])
    type = SelectField('Type', validators=[DataRequired()], choices=[("poet", "Poet"), ("reader", "Reader")])
    submit = SubmitField('Sign In')


# class ResetForm(FlaskForm):
#     email = EmailField('Email', validators=[DataRequired(), Email()])
#     # new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm', message="Passwords must match")])
#     # confirm_password = P
#     submit = SubmitField('Reset')