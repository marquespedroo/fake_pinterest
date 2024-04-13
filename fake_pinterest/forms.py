from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fake_pinterest.models import User

class FormLogin(FlaskForm):
    email = StringField("E-mail",validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmation_button = SubmitField("Log in")

    def validate_email(self,email):
        email_value = email.data
        user = User.query.filter_by(email=email_value).first()
        if not user:
            raise ValidationError("User does not exist. Please, create an account.")

class FormCreateAccount(FlaskForm):
    email = StringField("E-mail",validators=[DataRequired(), Email()])
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6,20)])
    password_confirmation =PasswordField("Repeat your password", validators=[DataRequired(),EqualTo("password")])
    confirmation_button = SubmitField("Create account")

    def validate_email(self,email):
        email_value = email.data
        user = User.query.filter_by(email=email_value).first()
        if user:
            raise ValidationError("You already have an account. Please, log in.")
        
    def validate_username(self,username):
        username_value = username.data
        user = User.query.filter_by(username=username_value).first()
        if user:
            raise ValidationError("This username is unavailable. Please, choose another one.")
        
class FormPhoto(FlaskForm):
    photo = FileField("Photo")
    confirmation_button = SubmitField("Upload photo", validators=[DataRequired()])
