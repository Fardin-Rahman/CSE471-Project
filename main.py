from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/scholarsync'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'thisisasecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class Contacts(db.Model, UserMixin):
    serialno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(12), nullable=False)

    def get_id(self):
        return str(self.serialno)

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



# @login_manager.user_loader
# def load_user(id):
#     return contacts.query.get(int(id))

@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')


@app.route("/courses")
def courses():
    return render_template('courses.html')

@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html')

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
        email_in= request.form.get('email')
        password_in= request.form.get('password')
        res = Contacts.query.filter(Contacts.email==email_in).all()
        if len(res) == 0:
            return 'error'  #need yo add flash on top
        elif res[0].email==email_in and res[0].password==password_in:
            login_user(res[0])
            return redirect(url_for('user'))
        elif res[0].email==email_in and res[0].password!=password_in:
            return 'password error' #need yo add flash on top

    return render_template('login.html')

@app.route("/job", methods= ['GET'])
def job(): #access database jobs
    res = Jobs.query.filter().all()
    return render_template('recruiters.html', result=res)


@app.route("/scholarship", methods= ['GET'])
def scholarship(): #access database
    res = Scholarship.query.filter().all()
    return render_template('scholarship.html', result=res)

@app.route("/prof")
def prof():
    return render_template('prof.html')




@login_manager.user_loader
def load_user(user_id):
    return Contacts.query.get(int(user_id))


@app.route('/user', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('user.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



if __name__ == "__main__":
    with app.test_request_context():
        app.add_url_rule('/login.html', 'login', login)
        app.add_url_rule('/index.html', '/', home)
        app.add_url_rule('/courses.html', 'courses', courses)
        app.add_url_rule('/jobs.html', 'job', job)
        app.add_url_rule('/recurments.html', 'recruiters', recruiters)
        app.add_url_rule('/contact.html', 'more', contact)
        app.add_url_rule('/user.html', 'user', user)
        app.add_url_rule('/aboutus.html', 'aboutus', aboutus)
        app.add_url_rule('/scholarship.html', 'scholarship', scholarship)
        app.add_url_rule('/prof.html', 'prof', prof)

    app.run(debug=True)


#----------------------------------------------------------------



