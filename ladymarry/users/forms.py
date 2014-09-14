import datetime

from flask_wtf import Form
from wtforms import DateField, StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, ValidationError

__all__ = ['RegisterForm', 'UpdateForm']

def _wedding_date_check(form, field):
    if field.data and field.data < datetime.date.today():
        raise ValidationError('Wedding date should be a future date.')

def _default_wedding_date():
    now = datetime.datetime.now()
    return datetime.date(now.year + 1, now.month, now.day)        


class RegisterForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[Optional(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    wedding_date = DateField(
        'Wedding Date',
        default=_default_wedding_date(),
        validators=[_wedding_date_check])


class UpdateForm(Form):
    email = StringField('Email', validators=[Email(), Optional()])
    first_name = StringField('First Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[Optional()])
    wedding_date = DateField(
        'Wedding Date',
        validators=[_wedding_date_check, Optional()])
    
