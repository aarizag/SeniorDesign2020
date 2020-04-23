from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class BusinessForm(FlaskForm):
    businessName = StringField('BusinessName', validators=[DataRequired()])
    submit = SubmitField('Check')
