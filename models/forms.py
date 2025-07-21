from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, NumberRange,InputRequired


class MyForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()]
                       , render_kw={"placeholder": "Username", 'id': "username"})
    email = EmailField('Email', validators=[DataRequired(), Email()]
                       , render_kw={"placeholder": "Enter your email", 'id': "useremail"}
                       , description="Please enter a valid email address")
    submit = SubmitField('Submit')


class HealthDataForm(FlaskForm):
    """Form for health data submission"""
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired(), InputRequired()])
    exercise = IntegerField('Exercise (minutes)', validators=[InputRequired(), NumberRange(min=0)])
    sleep = IntegerField('Sleep (hours)', validators=[InputRequired(), NumberRange(min=0, max=24)])
    meditation = IntegerField('Meditation (minutes)', validators=[InputRequired(), NumberRange(min=0)])
    blood_pressure = StringField('Blood Pressure (mmHg)', validators=[InputRequired()])
    submit = SubmitField('Submit')