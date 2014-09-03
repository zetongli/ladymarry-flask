from flask_wtf import Form
from wtforms import DateField, StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

__all__ = ['RegisterForm']


class RegisterForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    wedding_date = DateField('Wedding Date', validators=[DataRequired()])
