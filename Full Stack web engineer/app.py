from flask import Flask, render_template, redirect, url_for,flash, Blueprint,request ,send_file
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SelectField , FieldList ,FormField ,IntegerField , FloatField ,validators,Form, TextField, TextAreaField, validators, StringField, SubmitField,DateField,HiddenField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms_components import TimeField 
from flask import Flask, render_template
from flask_wtf import Form 
import matplotlib as plt
from flask_admin import Admin, BaseView, expose
#from wtforms import DateTimeField
from wtforms.fields.html5 import DateTimeField
from manipulationDB import pssw,existlogin,get_id,changeDB_clock_out,changeDB_clock_in,missedclock_mail,missedclock_boolean,get_date,changeDB_hours ,get_reports,get_report_spend_time,get_report_spend_times,get_report_spend_time_name,get_report_spend_times_name,addAttendanceValidator,get_hours_work

#import ldap
from flask_table import Table, Col
from manipulationDB import get_table_clock ,get_Monthly_Recap,get_table_AttendanceValidator,get_table_Attendance,update_Attendance,get_list_teamleader,get_table_new_attendences,addVacancyValidator,get_table_new_Vacancy,get_table_vacances,update_Vacancy,delete_Vacancy,delete_Attendance,get_hours_vacation

from wtforms import Form, DateField 
from wtforms_components import TimeField 
from time import gmtime, strptime
import numpy as np
from math import *
import os
import sys
#from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
from writeexcel import excel ,excelmonth
#from sendmail import sendmail


# config
app = Flask(__name__,static_folder=os.path.abspath("static/"))
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=600
)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!' #used to encrypt your cookies and save send them to the browser
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/redmine'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
bootstrap = Bootstrap(app)
sys.path.append('C:/Users/bigbooss/Desktop/feres_project-v2/classes/')
import login as log

def get_ldap_connection(user,mdp):
    return True
    conn = ldap.initialize('ldap://172.16.1.254')   
    conn.protocol_version = 3   
    conn.set_option(ldap.OPT_REFERRALS, 0)
    user=user+'@primatec.local'
    print (user)
    conn.simple_bind_s(user,mdp)
    print('connect')

class Users(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(15), unique=True)
    hashed_password = db.Column(db.String(80))
    firstname = db.Column(db.String(80))
    admin =db.Column(db.Integer)
    
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True

    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
    def is_admin(self):
        return(self.admin==1)

@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static', 'js'),   filename) 
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
@app.route('/')
def index():
   return redirect(url_for('login'))
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method=='POST':
        print request.form['username'],request.form['password']
        try :
                get_ldap_connection(request.form['username'],request.form['password'])
        except :
                flash('Invalid username or password')
                return render_template('login.html')
        
        user = Users.query.filter_by(login=request.form['username']).first()
        #login_user(user, remember=form.remember.data)
        if user.admin==1 :
             return redirect(url_for('dashboard'))
        else :
             return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')
 
if __name__ == '__main__':
    app.run(host="127.0.0.2",port='8050',debug=True)
