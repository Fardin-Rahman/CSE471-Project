 from flask import Flask, render_template,  request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/scholarsync'
db = SQLAlchemy(app)


class Contacts(db.Model):
    serialno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(12), nullable=False)
class Jobs(db.Model):
    Job_Code = db.Column(db.Integer, primary_key=True)
    Job_Title = db.Column(db.String(50), nullable=True)
    Company_Name = db.Column(db.String(50), nullable=False)
    Requirement = db.Column(db.String(50), nullable=True)
    Location = db.Column(db.String(50), nullable=False)
    Deadline = db.Column(db.String(50), nullable=False)

class Scholarship(db.Model):
    sc_code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    university = db.Column(db.String(50), nullable=False)
    requirement = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(200), nullable=False)






@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')


@app.route("/courses")
def courses():
    return render_template('courses.html')


@app.route("/recruiters")
def recruiters():
    return 'on process'



@app.route("/contact", methods = ['GET', 'POST']) #need to add more parameters for student sign up
def contact():
    try:
        if(request.method=='POST'):
            '''Add entry to the database'''
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            entry = Contacts(name=name,email = email, password=password )
            db.session.add(entry)
            db.session.commit()
        return render_template('contact.html')
    except:
        return render_template('contact_error.html')



@app.route("/user")
def user():
    return render_template('user.html')


@app.route("/login", methods= ['GET', 'POST'])
def login():
    if(request.method== 'POST'):
        '''Fetch data and add it to the database'''
        email= request.form.get('email')
        password= request.form.get('password')
        entry = Contacts(email=email, password= password)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('user'))  # Redirect to user.html after successful login

    return render_template('login.html')

@app.route("/job", methods= ['GET'])
def job(): #access database jobs
    res = Jobs.query.filter().all()
    return render_template('recruiters.html', result=res)


@app.route("/scholarship", methods= ['GET'])
def scholarship(): #access database
    res = Scholarship.query.filter().all()
    return render_template('scholarship.html', result=res)



if __name__ == "__main__":
    with app.test_request_context():
        app.add_url_rule('/login.html', 'login', login)
        app.add_url_rule('/index.html', '/', home)
        app.add_url_rule('/courses.html', 'courses', courses)
        app.add_url_rule('/jobs.html', 'job', job)
        app.add_url_rule('/recurments.html', 'recruiters', recruiters)
        app.add_url_rule('/contact.html', 'more', contact)
        app.add_url_rule('/user.html', 'user', user)
        app.add_url_rule('/scholarship.html', 'scholarship', scholarship)

    app.run(debug=True)






