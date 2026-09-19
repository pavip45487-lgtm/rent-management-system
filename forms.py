from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DecimalField, IntegerField, FileField, MultipleFileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 128)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Full Name', validators=[Optional(), Length(0, 120)])
    phone = StringField('Phone', validators=[Optional(), Length(0,20)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PropertyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1,200)])
    description = TextAreaField('Description', validators=[Optional()])
    purpose = SelectField('Purpose', choices=[('rent','Rent'),('sale','Sale')], validators=[Optional()])
    property_type = SelectField('Property Type', choices=[('apartment','Apartment'),('house','House'),('studio','Studio'),('villa','Villa')], validators=[Optional()])
    price = DecimalField('Price', validators=[Optional(), NumberRange(min=0)])
    deposit = DecimalField('Deposit', validators=[Optional(), NumberRange(min=0)])
    bedrooms = IntegerField('Bedrooms', validators=[Optional(), NumberRange(min=0)])
    bathrooms = IntegerField('Bathrooms', validators=[Optional(), NumberRange(min=0)])
    balcony = IntegerField('Balcony', validators=[Optional(), NumberRange(min=0)])
    parking = StringField('Parking', validators=[Optional(), Length(0,50)])
    area_size = StringField('Area', validators=[Optional(), Length(0,50)])
    floor = StringField('Floor', validators=[Optional(), Length(0,50)])
    facing = StringField('Facing', validators=[Optional(), Length(0,50)])
    furnished = StringField('Furnished', validators=[Optional(), Length(0,50)])
    water = StringField('Water', validators=[Optional(), Length(0,50)])
    electricity = StringField('Electricity', validators=[Optional(), Length(0,50)])
    internet = StringField('Internet', validators=[Optional(), Length(0,50)])
    address = StringField('Address', validators=[Optional(), Length(0,255)])
    locality = StringField('Locality/Area', validators=[Optional(), Length(0,120)])
    city = StringField('City', validators=[Optional(), Length(0,120)])
    district = StringField('District', validators=[Optional(), Length(0,120)])
    state = StringField('State', validators=[Optional(), Length(0,120)])
    pincode = StringField('Pincode', validators=[Optional(), Length(0,20)])
    google_map = StringField('Google Map Link', validators=[Optional(), Length(0,255)])
    owner_name = StringField('Owner Name', validators=[Optional(), Length(0,120)])
    owner_phone = StringField('Owner Phone', validators=[Optional(), Length(0,50)])
    owner_email = StringField('Owner Email', validators=[Optional(), Email()])
    available_from = StringField('Available From', validators=[Optional(), Length(0,50)])
    images = MultipleFileField('Property Images', validators=[Optional()])
    submit = SubmitField('Save')

class SearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[Optional(), Length(0,200)])
    city = StringField('City', validators=[Optional(), Length(0,120)])
    property_type = SelectField('Property Type', choices=[('','Any type'),('apartment','Apartment'),('house','House'),('studio','Studio'),('villa','Villa')], validators=[Optional()])
    bedrooms = IntegerField('Bedrooms', validators=[Optional(), NumberRange(min=0)])
    min_price = DecimalField('Min Price', validators=[Optional()])
    max_price = DecimalField('Max Price', validators=[Optional()])
    sort_by = SelectField('Sort by', choices=[('newest','Newest'),('price_low','Price: Low to High'),('price_high','Price: High to Low')], validators=[Optional()])
    submit = SubmitField('Search')

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(1,1000)])
    submit = SubmitField('Send')

class UpdateProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[Optional(), Length(0,120)])
    phone = StringField('Phone', validators=[Optional(), Length(0,20)])
    submit = SubmitField('Update')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(6,128)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(6,128)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Set Password')
