from flask_wtf import Form
from wtforms import StringField, TextAreaField, DateField, IntegerField
from wtforms.validators import (DataRequired, ValidationError,
                                Length, EqualTo)

from models import Entry

def title_exists(form, field):
    if Entry.select().where(Entry.title == field.data).exists():
        raise ValidationError("This title already exists.")


class EntryForm(Form):
    title = StringField("Title", validators=[
        DataRequired(), title_exists])
    created = DateField("Data", validators=[
        DataRequired()])
    time_spent = IntegerField("Time Spent", validators=[
        DataRequired()])
    learned = TextAreaField("What you learned", validators=[
        DataRequired()])
    to_remember = TextAreaField("Resources to remember",
                                validators=[DataRequired()])


