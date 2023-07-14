from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email



class RegForm(FlaskForm):
    username = StringField("username", validators=[InputRequired() ])
    password = PasswordField("password", validators=[InputRequired()])
    email = StringField("email", validators=[InputRequired(), Email() ])
    first_name = StringField("first name", validators=[InputRequired()])
    last_name = StringField("last name", validators=[InputRequired()])


class LoginForm(FlaskForm):
     username = StringField("username", validators=[InputRequired() ])
     password = PasswordField("password", validators=[InputRequired() ])


class FeedBackForm(FlaskForm):
    title = StringField("title", validators=[InputRequired() ])
    content = StringField("content", validators=[InputRequired()])

class FeedBackEditForm(FlaskForm):
    title = StringField("title", validators=[InputRequired() ])
    content = StringField("content", validators=[InputRequired()])
