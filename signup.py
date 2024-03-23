from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError


class signUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(4, 8)])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password',
                                    validators=[DataRequired()])
    agree = BooleanField('I agree to the terms and conditions', validators=[DataRequired()])
    submit = SubmitField('Register')

    db_email = ['abc@gmail.com', 'nishad@yahoo.com', 'sakib@hotmail.com']

    def validate_email(self, field):
        email = field.data
        for e in self.db_email:
            if e == email:
                raise ValidationError('Email already exists.')

    def validate_repeat_password(self, field):
        if field.data != self.password.data:
            raise ValidationError('Passwords did not match')