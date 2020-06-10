#!/usr/bin/python
#-*- coding: utf-8 -*-
import MySQLdb 
import time
from builtins import str
vacancy = ',(SELECT SUM(hours) FROM redmine.time_entries as a,  redmine.issues as b WHERE a.issue_id= b.id and b.tracker_id=13 and  a.user_id = d.id and a.spent_on = date(i.start_time)) as Vacancy '
def pssw(login) :
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
    c = bdd.cursor()
    cmd='SELECT hashed_password FROM users where login='+ '"'+login+'"'
    c.execute(cmd)
    results = c.fetchone()
    bdd.close()
    return(results[0])
    
def existlogin(login) :
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
    c = bdd.cursor()
    cmd='SELECT hashed_password FROM users where login='+ '"'+login+'"'
    c.execute(cmd)
    results = c.fetchone()
    bdd.close()
    return(results!=None,)
def get_date(id) :
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
    c = bdd.cursor()
    cmd='select start_time from wk_attendances where start_time=end_time and user_id=' + '"'+str(id)+'"'
    c.execute(cmd)
    results = c.fetchone()
    bdd.close()
    return(str(results[0]).split()[0])
def missedclock_boolean(id) :
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
    c = bdd.cursor()
    cmd='select start_time from wk_attendances where start_time=end_time and user_id=' + '"'+str(id)+'"'
    c.execute(cmd)
    results = c.fetchone()
    bdd.close()
    return(results!=None)
def missedclock_mail() :
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
    c = bdd.cursor()
    cmd='SELECT address FROM email_addresses where user_id in (select user_id from wk_attendances where start_time=end_time)'
    c.execute(cmd)
    results = c.fetchall()
    bdd.close()
    return(results)
def changeDB_clock_out(time,id):
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
    c = bdd.cursor()
    cmd='UPDATE wk_attendances set end_time ='+ '"'+time+'"'+' where id='+'"'+str(id)+'"'

    c.execute(cmd)
    bdd.commit()
    bdd.close()
def changeDB_clock_in(time,id):
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
    c = bdd.cursor()
    cmd='UPDATE wk_attendances set start_time ='+ '"'+time+'"'+' where id='+'"'+str(id)+'"'

    c.execute(cmd)
    bdd.commit()
    bdd.close()
def changeDB_hours(hour,id):
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
    c = bdd.cursor()
    cmd='UPDATE wk_attendances set hours ='+ '"'+str(hour)+'"'+' where id='+'"'+str(id)+'"'
    c.execute(cmd)
    bdd.commit()
    bdd.close()
 
def addVacancyValidator(start_time, end_time, user_validator, type_vacancy,nbr_jour,user_id):
    
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
    c = bdd.cursor() 
    cmd = 'INSERT INTO vacancy_validator (start_time, end_time, user_validator, status_validator, type_vacancy,nbr_jour,user_id) VALUES ("'+start_time+'", "'+end_time+'", "'+user_validator+'","wait","'+type_vacancy+'",'+nbr_jour+','+user_id+');'
    c.execute(cmd)
    bdd.commit()
    bdd.close()
   
def addAttendanceValidator(id_attendance, new_start_time, new_end_time, user_validator,hours_validator,user_id):
    
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
    c = bdd.cursor()
    
    if id_attendance == 0:
        cmd = 'INSERT INTO attendances_validator (id_attendance, new_start_time, new_end_time, user_validator, status_validator,hours_validator,user_id,updated_at) VALUES (NULL, "'+new_start_time+'", "'+new_end_time+'", "'+user_validator+'","wait",'+hours_validator+','+user_id+',NOW());'
        c.execute(cmd)
        bdd.commit()
    else:
   
        cmd1= 'select * from attendances_validator where id_attendance= '+id_attendance
        rows_count = c.execute(cmd1)
        if rows_count< 1:
            
        
            #cmd='UPDATE wk_attendances set hours ='+ '"'+str(hour)+'"'+' where id='+'"'+str(id)+'"'
            cmd = 'INSERT INTO attendances_validator (id_attendance, new_start_time, new_end_time, user_validator, status_validator,hours_validator,user_id,updated_at) VALUES ('+id_attendance+', "'+new_start_time+'", "'+new_end_time+'", "'+user_validator+'","wait",'+hours_validator+','+user_id+',NOW());'
            c.execute(cmd)
            bdd.commit()
    bdd.close()
    
def get_table_new_Vacancy(id_user):
  bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
  c = bdd.cursor()
  #cmd = 'SELECT new_start_time ,new_end_time,id_attendance,hours_validator  FROM wk_attendances where user_id='+ '"'+str(id_user)+'"'+'order by id'
  cmd='SELECT start_time ,end_time,id,nbr_jour,status_validator FROM redmine.vacancy_validator where   user_id= '+ '"'+str(id_user)+'"'+' ;'
  c.execute(cmd)
  results = c.fetchall()
  bdd.close()
  return(results)

def get_table_new_attendences(id_user):
  bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
  c = bdd.cursor()
  #cmd = 'SELECT new_start_time ,new_end_time,id_attendance,hours_validator  FROM wk_attendances where user_id='+ '"'+str(id_user)+'"'+'order by id'
  cmd='SELECT new_start_time ,new_end_time,id_attendance,hours_validator FROM redmine.attendances_validator where id_attendance is null and user_id= '+ '"'+str(id_user)+'"'+' ;'
  c.execute(cmd)
  results = c.fetchall()
  bdd.close()
  return(results)

def get_table_AttendanceValidator(id_user):
  bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
  c = bdd.cursor()
  #cmd = 'SELECT new_start_time ,new_end_time,id_attendance,hours_validator  FROM wk_attendances where user_id='+ '"'+str(id_user)+'"'+'order by id'
  cmd='SELECT new_start_time ,new_end_time,id_attendance,hours_validator  FROM redmine.attendances_validator as a,  redmine.wk_attendances as b where b.user_id = '+ '"'+str(id_user)+'"'+' and a.id_attendance=b.id;'
  c.execute(cmd)
  results = c.fetchall()
  bdd.close()
  return(results)
  
def get_table_vacances(login):
  bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
  c = bdd.cursor()
  #cmd='SELECT new_start_time ,new_end_time,id_attendance,hours_validator,c.login  FROM redmine.attendances_validator as a, redmine.wk_attendances as b , redmine.users as c where c.id = b.user_id and b.id=a.id_attendance and a.status_validator="wait" and a.user_validator =  "'+login+'";'
  cmd='SELECT id,start_time ,end_time,nbr_jour,(select login from redmine.users where id=user_id) as login  FROM redmine.vacancy_validator where status_validator="wait" and user_validator = "'+login+'";'
  c.execute(cmd)
  results = c.fetchall()
  bdd.close()
  return(results)
  
def get_table_Attendance(login):
  bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
  c = bdd.cursor()
  #cmd='SELECT new_start_time ,new_end_time,id_attendance,hours_validator,c.login  FROM redmine.attendances_validator as a, redmine.wk_attendances as b , redmine.users as c where c.id = b.user_id and b.id=a.id_attendance and a.status_validator="wait" and a.user_validator =  "'+login+'";'
  cmd='SELECT id,new_start_time ,new_end_time,id_attendance,hours_validator,(select login from redmine.users where id=user_id) as login , updated_at FROM redmine.attendances_validator where status_validator="wait" and user_validator = "'+login+'";'
  c.execute(cmd)
  results = c.fetchall()
  bdd.close()
  return(results)

def update_Vacancy(id_adapter):
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
    c = bdd.cursor()
    cmd='UPDATE redmine.vacancy_validator SET status_validator = "validate"  WHERE (id = '+id_adapter+');'
    c.execute(cmd)
    bdd.commit()
    bdd.close()
    
def delete_Vacancy(id_adapter):
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
    c = bdd.cursor()
    cmd='DELETE FROM redmine.vacancy_validator  WHERE id = '+id_adapter+';'
    c.execute(cmd)
    bdd.commit()
    bdd.close()


def delete_Attendance(id_adapter,user_login,new_start,new_end,hours,x,updated_at):
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
    c = bdd.cursor()
    cmd='DELETE FROM redmine.attendances_validator   WHERE id = '+id_adapter+';'
    c.execute(cmd)
    bdd.commit()
    bdd.close()

def update_Attendance(id_adapter,user_login,new_start,new_end,hours,x,updated_at):
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
    c = bdd.cursor()
    if x == "None" :
        cmd_insert = 'INSERT INTO redmine.wk_attendances (user_id,start_time, end_time, hours, created_at, updated_at) VALUES ((select id from redmine.users where login= "'+user_login+'"), "'+new_start+'", "'+new_end+'", '+hours+',"'+updated_at+'","'+updated_at+'");'
        c.execute(cmd_insert)
        bdd.commit()
        
        
        
        cmd='UPDATE redmine.attendances_validator SET status_validator = "validate" , id_attendance= (SELECT id FROM redmine.wk_attendances  ORDER BY ID DESC LIMIT 1)  WHERE (id = '+id_adapter+');'
        c.execute(cmd)
        
    else :
        
        cmd='UPDATE redmine.attendances_validator SET status_validator = "validate" WHERE (id_attendance = '+x+');'
        cmd1='UPDATE redmine.wk_attendances SET start_time = "'+new_start+'" , end_time="'+new_end+'" , hours='+hours+' WHERE (id = "'+x+'");'
        c.execute(cmd)
        c.execute(cmd1)
    bdd.commit()
    bdd.close()

def get_id(login) :
  bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
  c = bdd.cursor()
  cmd = 'SELECT id FROM users where login='+ '"'+login+'"'
  c.execute(cmd)
  results = c.fetchone()
  bdd.close()
  return(results[0])
  
def get_list_teamleader():
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
    c = bdd.cursor()
    cmd = 'SELECT id,login FROM redmine.users  where id in (select user_id from redmine.groups_users where group_id = (SELECT id FROM redmine.users where type ="Group" and lastname="AllLeaders"))'
    c.execute(cmd)
    results = c.fetchall()
    bdd.close()
    return(results)


def get_mail(id_user):
  bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
  c = bdd.cursor()
  cmd = 'SELECT address FROM email_addresses where user_id='+ '"'+str(id_user)+'"'
  c.execute(cmd)
  results = c.fetchone()
  bdd.close()
  return(results[0])
  
def get_table_clock(id_user):
  bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
  c = bdd.cursor()
  if id_user!="" :
      cmd = 'SELECT start_time ,end_time,id,hours  FROM  wk_attendances where user_id='+ '"'+str(id_user)+'"'+'order by id'
  else :
      cmd = 'SELECT login,start_time ,end_time,a.id,hours  FROM users, wk_attendances as a order by id limit 100'
  print cmd
  c.execute(cmd)
  results = c.fetchall()
  bdd.close()
  return(results)

  


def get_reports(date) :
  bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
  c = bdd.cursor()
  cmd = 'SELECT  d.id, user_id,login ,start_time,end_time,hours  FROM wk_attendances as i ,users as d where i.user_id=d.id and  i.start_time LIKE'+ '"'+str(date)+'%'+'"'
  c.execute(cmd)
  results = c.fetchall()
  bdd.close()
  return(results)
  
  
def get_report_spend_times(dateDebut,dateFin) :
  bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
  c = bdd.cursor()
  cmd = 'SELECT d.id,user_id, login, start_time,end_time,hours, (SELECT SUM(hours)  FROM redmine.time_entries as a,  redmine.issues as b WHERE a.issue_id= b.id and b.tracker_id!=13 and  a.user_id = d.id and a.spent_on = date(i.start_time)) as timespent '+vacancy+' FROM redmine.wk_attendances AS i,redmine.users AS d WHERE   i.user_id = d.id   AND date(i.start_time) >= '+ '"'+str(dateDebut)+'" AND date(i.start_time) <= '+'"'+str(dateFin)+'"'
  #cmd = 'SELECT d.id,user_id, login, start_time,end_time,hours, (SELECT SUM(hours) FROM redmine.time_entries WHERE  spent_on = date(i.start_time) AND user_id = d.id) as timespent FROM redmine.wk_attendances AS i,redmine.users AS d WHERE   i.user_id = d.id   AND date(i.start_time) >= '+ '"'+str(dateDebut)+'" AND date(i.start_time) <= '+'"'+str(dateFin)+'"'
  c.execute(cmd)
  results = c.fetchall()
  bdd.close()
  return(results)
  
def get_report_spend_times_name(dateDebut,dateFin,loginname) :
  bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
  c = bdd.cursor()
  cmd = 'SELECT d.id,user_id, login, start_time,end_time,hours, (SELECT SUM(hours) FROM redmine.time_entries as a,  redmine.issues as b WHERE a.issue_id= b.id and b.tracker_id!=13 and  a.user_id = d.id and a.spent_on = date(i.start_time)) as timespent  '+vacancy+'  FROM redmine.wk_attendances AS i,redmine.users AS d WHERE    d.login='+'"' +loginname + '"  AND i.user_id = d.id AND date(i.start_time) >= '+ '"'+str(dateDebut)+'" AND date(i.start_time) <= '+'"'+str(dateFin)+'"'
  c.execute(cmd)
  results = c.fetchall()
  bdd.close()
  return(results)

def get_report_spend_time(date) :
  bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
  c = bdd.cursor()
  cmd = 'SELECT d.id,user_id, login, start_time,end_time,hours, (SELECT SUM(hours) FROM redmine.time_entries WHERE  spent_on = '+ '"'+str(date)+'"'+' AND user_id = d.id) as timespent FROM redmine.wk_attendances AS i,redmine.users AS d WHERE   i.user_id = d.id   AND i.start_time LIKE '+ '"'+str(date)+'%'+'"'
  c.execute(cmd)
  results = c.fetchall()
  bdd.close()
  return(results)

def get_report_spend_time_name(loginname) :
  bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
  c = bdd.cursor()
  cmd = 'SELECT d.id,user_id, login, start_time,end_time,hours, (SELECT SUM(hours) FROM redmine.time_entries as a,  redmine.issues as b WHERE a.issue_id= b.id and b.tracker_id!=13 and  a.user_id = d.id and a.spent_on= date(start_time)) as timespent  '+vacancy+'  FROM redmine.wk_attendances AS i,redmine.users AS d WHERE    d.login = '+'"'+loginname+'"'
  c.execute(cmd)
  results = c.fetchall()
  bdd.close()
  return(results)
  
def get_report_spend_time() :
  bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
  c = bdd.cursor()
  #cmd = 'SELECT d.id,user_id, login, start_time,end_time,hours, (SELECT SUM(hours) FROM redmine.time_entries WHERE  user_id = d.id and spent_on= date(start_time)) as timespent FROM redmine.wk_attendances AS i,redmine.users AS d WHERE   i.user_id = d.id  '
  cmd='SELECT d.id,user_id, login, start_time,end_time,hours, (SELECT SUM(hours) FROM redmine.time_entries as a,  redmine.issues as b WHERE a.issue_id= b.id and b.tracker_id!=13 and  a.user_id = d.id and a.spent_on= date(start_time)) as timespent  '+vacancy+'  FROM redmine.wk_attendances AS i,redmine.users AS d WHERE   i.user_id = d.id  '
  c.execute(cmd)
  results = c.fetchall()
  bdd.close()
  return(results)
  
def get_Monthly_Recap(date) :
  bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
  c = bdd.cursor()
  cmd = 'SELECT  d.firstname,d.lastname, sum(hours)  FROM wk_attendances as i ,users as d where i.user_id=d.id and  i.start_time LIKE'+ '"'+str(date)+'%'+'"'+'group by user_id'
  c.execute(cmd)
  results = c.fetchall()
  bdd.close()
  return(results)
  
  
def get_hours_vacation(user_id):
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
    c = bdd.cursor()
    cmd='SELECT sum(nbr_jour) FROM redmine.vacancy_validator where user_id = '+str(user_id)+' and YEAR(start_time)=year(now()) and status_validator="validate";'
    c.execute(cmd)
    results = c.fetchone()
    bdd.close()
    return(results[0])

def get_vacation_validate_day(user_id,date):
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
    c = bdd.cursor()
    cmd='SELECT COALESCE(sum(nbr_jour),0) FROM redmine.vacancy_validator where user_id = '+str(user_id)+' and date(start_time)="'+str(date)+'" and status_validator="validate"'
    print(cmd)
    c.execute(cmd)
    results = c.fetchone()
    bdd.close()
    print(results[0])
    return(results[0])

def get_hours_work(user_id):
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine");
    c = bdd.cursor()
    cmd='SELECT user_id,TIMEDIFF(end_time,start_time),hours   FROM redmine.wk_attendances where user_id='+str(user_id)+' and YEAR(start_time)=year(now())'
    c.execute(cmd)
    results = c.fetchall()
    bdd.close()
    return(results)
def get_hours_work(user_id):
    bdd = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="redmine")
    c = bdd.cursor()
    cmd = "DELETE FROM wk_attendances WHERE condition"
if __name__=='__main__' :
  print((Monthly_Recap('2018-06') ))
  
