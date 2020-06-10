from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sys
sys.path.append('/home/feres_project-v2')
from flask_sqlalchemy  import SQLAlchemy
from app import db,SQLAlchemy
print 1
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=80)])
    remember = BooleanField('remember me')   
