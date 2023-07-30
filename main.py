from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql
import datetime
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
login_manager.login_view = 'loginP'



class Contacts(db.Model, UserMixin):
    serialno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(12), nullable=False)

    def get_id(self):
        return str(self.serialno)

class Profcontacts(db.Model, UserMixin):
    serial = db.Column(db.Integer, primary_key=True)
    FullName = db.Column(db.String(100), nullable=False)
    uniName = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(120), unique=True, nullable=False)
    passw = db.Column(db.String(100), nullable=False)

    def get_id(self):
        return str(self.serial)

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

class Query(db.Model):
    q_id= db.Column(db.Integer, primary_key=True)
    question= db.Column(db.String(250),nullable=False)

class Reply(db.Model):
    r_id= db.Column(db.Integer, nullable=False)
    answer = db.Column(db.String(250), nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    ans_id = db.Column(db.Integer, primary_key=True)
import enum

class WishlistStatus(enum.Enum):
    no = 'no'
    yes = 'yes'

class CartStatus(enum.Enum):
    no = 'no'
    yes = 'yes'

class Premium(db.Model):
    c_id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(250), nullable=False)
    wishlist = db.Column(db.Enum(WishlistStatus), nullable=False, default=WishlistStatus.no)
    cart = db.Column(db.Enum(CartStatus), nullable=False, default=CartStatus.no)

    def __init__(self, c_name, wishlist=WishlistStatus.no, cart=CartStatus.no):
        self.c_name = c_name
        self.wishlist = wishlist
        self.cart = cart

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


@app.route("/profcontact", methods = ['GET', 'POST']) #need to add more parameters for student sign up
def profcontact():
    try:
        if(request.method=='POST'):
            '''Add entry to the database'''
            FullName = request.form.get('FullName')
            uniName=request.form.get("uniName")
            designation=request.form.get("designation")
            mail = request.form.get('mail')
            passw = request.form.get('passw')

            entry = Profcontacts(FullNamename=FullName,mail = mail, passw=passw,uniName=uniName,designation=designation )
            db.session.add(entry)
            db.session.commit()
        return render_template('profcontact.html')
    except:
        return render_template('contact_error.html')






@app.route("/user")
def user():
    return render_template('user.html')

@app.route("/userP")
def userP():
    return render_template('userP.html')


@app.route("/login", methods= ['GET', 'POST'])
def login():
    if(request.method== 'POST'):
        email_in= request.form.get('email')
        password_in= request.form.get('password')
        res = Contacts.query.filter(Contacts.email==email_in).all()
        if len(res) == 0:
            #return render_template("userP.html")
            return 'errorwdwefw'  #need to add flash on top
        elif res[0].email==email_in and res[0].password==password_in:
            login_user(res[0])
            return redirect(url_for('user'))
        elif res[0].email==email_in and res[0].password!=password_in:
            return 'password error' #need to add flash on top

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

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route("/premium")
def premium():
    return render_template('premium.html')

@app.route("/discussion", methods = ['GET', 'POST'])
def Discussion():
    ques = Query.query.filter().all()
    rep = Reply.query.filter().all()
    if (request.method == 'POST'):
        q = request.form.get('q')
        id = request.form.get('r_id')
        r = request.form.get('r')
        print(r)
        if q!=None and len(q) > 0:
            entry = Query(question=q)
            db.session.add(entry)
            db.session.commit()
        elif r!=None and len(r) > 0:
            entry = Reply(r_id=id, answer=r)
            db.session.add(entry)
            db.session.commit()
        return redirect('/discussion')
    return render_template('discussion.html', ques=ques, reply=rep)
#@app.route('/loginP')
#def loginP():
    #return render_template('loginP.html')
@app.route("/loginP", methods= ['GET', 'POST'])
def loginP():
    if(request.method== 'POST'):
        mail_in= request.form.get('mail')
        passw_in= request.form.get('password')
        res = Profcontacts.query.filter(Profcontacts.mail==mail_in).all()
        print(mail_in,passw_in,res[0].mail)
        if len(res) == 0:
            return 'error'  #need to add flash on top
        elif res[0].mail==mail_in and res[0].passw==passw_in:
            login_user(res[0])
            return redirect(url_for('userP'))
        elif res[0].mail==mail_in and res[0].passw!=passw_in:

            return 'password error' #need to add flash on top

    return render_template('loginP.html')


'''
@app.route("/loginP", methods=['GET', 'POST'])
def loginP():
    if request.method == 'POST':
        mail_in = request.form.get('mail')
        passw_in = request.form.get('passw')
        res = Profcontacts.query.filter_by(mail=mail_in).first()

        if not res:
            flash('Invalid email or password', 'error12')
            return redirect(url_for('loginP'))

        if res.passw == passw_in:
            login_user(res)
            return redirect(url_for('dashboard2'))

        flash('Invalid email or password', 'error12')
        return redirect(url_for('loginP'))

    return render_template('loginP.html')'''

'''
@app.route("/loginP", methods=['GET', 'POST'])
def loginP():
    if (request.method == 'POST'):
        #Fetch data and add it to the database
        FullName = request.form.get('FullName')
        uniName = request.form.get("uniName")
        designation = request.form.get("designation")
        mail = request.form.get('mail')
        passw = request.form.get('passw')
        entry = Profcontacts(FullNamename=FullName,mail = mail, passw=passw,uniName=uniName,designation=designation )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('userP'))  # Redirect to user.html after successful login

    return render_template('loginP.html')'''


@login_manager.user_loader
def load_user2(user_id2):
    return Profcontacts.query.get(int(user_id2))


@app.route('/userP', methods=['GET', 'POST'])
@login_required
def dashboard2():
    return render_template('userP.html')


@login_manager.user_loader
def load_user(user_id2):
    return Profcontacts.query.get(int(user_id2))


@app.route('/user', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('user.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/premium')
def premium():
    # Fetch courses from the database
    courses = Premium.query.all()
    total_courses_in_cart = sum(1 for course in courses if course.cart == CartStatus.yes)
    return render_template('premium.html', courses=courses, total_courses_in_cart=total_courses_in_cart)


@app.route('/add_course', methods=['POST'])
def add_course():
    course_name = request.form['course_name']
    wishlist_status = request.form.get('wishlist', 'no')
    cart_status = request.form.get('cart', 'no')

    wishlist_status = WishlistStatus.yes if wishlist_status == 'yes' else WishlistStatus.no
    cart_status = CartStatus.yes if cart_status == 'yes' else CartStatus.no

    course = Premium(c_name=course_name, wishlist=wishlist_status, cart=cart_status)
    db.session.add(course)
    db.session.commit()

    return "Course added successfully."


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
        app.add_url_rule('/userP.html', 'userP', userP)
        app.add_url_rule('/loginP.html','loginP', loginP)
        app.add_url_rule('/profcontact.html','profcontact', profcontact)
        app.add_url_rule('/premium.html', 'premium', premium)


    app.run(debug=True)


#----------------------------------------------------------------



