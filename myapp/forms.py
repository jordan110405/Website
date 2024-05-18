from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, RadioField
from wtforms.validators import DataRequired


class lost_and_found_form(FlaskForm):
    name = StringField('name-garage')
    picture = FileField('picture-garage')
    details = TextAreaField('details-garage')
    pickup_location = StringField('pickup-location-garage')
    contact_info = StringField('contact-info-garage')
    bounty = StringField('bounty-garage')


class ProductForm(FlaskForm):
    name = StringField('name')
    picture = FileField('picture')
    details = TextAreaField('details')
    pickup_location = StringField('pickup_location')
    contact_info = StringField('contact_info')
    rad_type = RadioField('Type', choices=[('items', 'Items'), ('services', 'Services')], validators=[DataRequired()])
