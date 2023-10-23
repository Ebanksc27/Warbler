from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional, URL

class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

# Updated to allow updates to profile info
class UserProfileForm(FlaskForm):
    """Form for updating user profile."""

    username = StringField('Username', validators=[DataRequired()])  # Added username field
    email = StringField('E-mail', validators=[DataRequired(), Email()])  # Added email field
    bio = TextAreaField('Bio', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])
    header_image_url = StringField('(Optional) Header Image URL', validators=[Optional(), URL()])
    image_url = StringField('(Optional) Image URL', validators=[Optional(), URL()])
    password = PasswordField('Current Password', validators=[DataRequired()])
