import datetime

from flask_wtf import Form
from wtforms import DateField, StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

__all__ = ['RegisterForm', 'UpdateForm']

def _wedding_date_check(form, field):
    if field.data and field.data < datetime.date.today():
        raise ValidationError('Wedding date should be a future date.')


class RegisterForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    wedding_date = DateField(
        'Wedding Date',
        validators=[_wedding_date_check])


class UpdateForm(Form):
    email = StringField('Email', validators=[Email()])
    first_name = StringField('First Name', validators=[])
    last_name = StringField('Last Name', validators=[])
    wedding_date = DateField(
        'Wedding Date',
        validators=[_wedding_date_check])
    
