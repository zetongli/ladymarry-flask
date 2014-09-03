import datetime

from flask_wtf import Form
from wtforms import DateField, StringField, PasswordField
from wtforms.validators import Required, Email, EqualTo, ValidationError

__all__ = ['RegisterForm']

def _wedding_date_check(form, field):
    if field.data and field.data < datetime.date.today():
        raise ValidationError('Wedding date should be a future date.')

def _default_wedding_date():
    now = datetime.datetime.now()
    return datetime.date(now.year + 1, now.month, now.day)
         

class RegisterForm(Form):
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[Required(), EqualTo('password')])
    first_name = StringField('First Name', validators=[Required()])
    last_name = StringField('Last Name', validators=[Required()])
    wedding_date = DateField(
        'Wedding Date',
        default=_default_wedding_date(),
        validators=[Required(), _wedding_date_check])



