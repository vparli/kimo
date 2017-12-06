# start of the "do not touch" section
from flask import Flask,render_template, request, flash, redirect, url_for, session, logging
import os
from urllib import parse
import psycopg2
import psycopg2.extras
import sys
from wtforms import Form, DateField, StringField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = 'lifeishard'

# start of database connection
def connectToDB():
    conn = psycopg2.connect(
        host = "ec2-54-225-88-191.compute-1.amazonaws.com",
        port = "5432",
        dbname = "d9km7fajl1oem0",
        user = "xbqulaeqyriama",
        password = "228fc56425ec433346270e4343fbba2217106e0d02136756ea6255888c4f14c8")
    c = conn.cursor()
    return conn, c

conn, c = connectToDB()
# end of the "do not touch" section


# start of routing views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Home')
def home():
    return render_template('home.html')



GENDEROPTIONS = ('SELECT', 'MALE', 'FEMALE')
#start of registration
class RegisterForm(Form):
    firstname = StringField('First Name', [validators.Length(min=1, max=50)])
    surname = StringField('Last Name', [validators.Length(min=1, max=50)])
    emailaddress = StringField('Email', [validators.Length(min=1, max=25)])
    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.EqualTo('confirm',message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    gender = SelectField(label='Gender',choices=[(gender,gender) for gender in GENDEROPTIONS])


@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        firstname = #kimo?
        surname = #kimo?
        emailaddress = #kimo?
        password = #kimo?
        gender = #kimo?
        #this will register a user to database

        SQL = '#kimo? VALUES (%s, %s, %s, %s, %s);'
        data = (firstname, surname, emailaddress, password, gender)
        c.execute(SQL,data)
        conn.commit()


        #go to login page if register successful, since user can login now
        return redirect(url_for('login'))

    return render_template('Register.html', form=form)
#end of registration

#start of login
@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        emailaddress = request.form['email']
        #candidate because input might be wrong, so it needs to be checked first
        password_candidate = request.form['password']

        SQLLOGIN = 'SELECT * FROM "USERDETAILS" WHERE email = %s;'
        additionals = (emailaddress)
        c.execute(""" SELECT * FROM "USERDETAILS" WHERE email = %s""", [emailaddress])

        for userrow in c.fetchall():
            print(userrow)
            users = 1

        # unhashing password
        if users == 1:
            datalogin = c.fetchall()
            password = userrow[4]

            #compare passwords
            if sha256_crypt.verify(password_candidate, password):
                print("Password Matched")

                session['logged-in'] = True
                session['username'] = userrow[1]
                session['userid'] = userrow[0]

                return redirect(url_for('home'))
            else:
                #print("Invalid password")
                error = 'Incorrect password'
                return render_template('Login.html', error=error)
        else:
            #print("invalid email")
            error = 'Username not found'
            return render_template('Login.html',error=error)

    return render_template('Login.html')
#end of login

class Academic(Form):
    university = #kimo?
    qual = #kimo?
    datestartedstudying = #kimo?
    datefinishedstudying = #kimo?


@app.route('/Academic',methods=['GET','POST'])
def academic():
    form = RegisterForm(request.form)
    if request.method == 'GET':
        try:
            #kimo? only one line
        except:
            print("Error executing sql statement")
        u = c.fetchall()

        return render_template('Academic.html',academicstuff=u)

    if request.method == 'POST':
        userid = session['userid']
        universityname = request.form['universityname']
        academicqualification = request.form['qualification']
        datestarteduniversity = request.form['datestartedstudying']
        dateendeduniversity = request.form['dateendedstudying']

        SQL = '#kimo? VALUES (%s, %s, %s, %s, %s);'
        data = (userid, universityname, academicqualification, datestarteduniversity, dateendeduniversity)
        c.execute(SQL, data)
        conn.commit()
        print("Academic Successfully Added")

        # go to login page if register successful, since user can login now
        return redirect(url_for('academic'))

    return render_template('Academic.html')

@app.route('/EditAcademic/<int:eid>',methods=['GET','POST'])
def editacademic(eid):

    #get academic record by id
    c.execute("""SELECT * FROM "ACADEMIC" WHERE academicid = %s""", [eid])
    records = c.fetchone()

    form = Academic(request.form)
    form.university.data = records[2]
    form.qual.data = records[3]
    form.datestartedstudying.data = records[4]
    form.datefinishedstudying.data = records[5]

    if request.method == 'POST' and form.validate():
        userid = session['userid']
        universityname = request.form['university']
        academicqualification = request.form['qual']
        datestarteduniversity = request.form['datestartedstudying']
        dateendeduniversity = request.form['datefinishedstudying']

        #kimo?
        conn.commit()
        print("Academic Successfully Updated")

        # go to login page if register successful, since user can login now
        return redirect(url_for('academic'))

    return render_template('editacademic.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)
    connectToDB()