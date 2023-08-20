from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql
import datetime
pymysql.install_as_MySQLdb()
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask import flash, session, render_template, request, redirect, url_for
import os
from datetime import date
course_taken = None
datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/scholarsync'
db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'thisisasecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# login_manager.login_view = 'loginP'

class Contacts(db.Model, UserMixin):
    serialno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(12), nullable=False)
    basic_mode = db.Column(db.Boolean, nullable=False, default=True)
    image = db.Column(db.String(80), nullable=False)
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

class Admin_login(db.Model, UserMixin):
    aserial = db.Column(db.Integer, primary_key=True)
    aname = db.Column(db.String(100), nullable=False)
    aemail = db.Column(db.String(120), unique=True, nullable=False)
    apassword = db.Column(db.String(100), nullable=False)
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
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    poster = db.Column(db.String(25), nullable=False)

class Reply(db.Model):
    r_id= db.Column(db.Integer, nullable=False)
    answer = db.Column(db.String(250), nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    ans_id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String(25), nullable=False)

class Prof_post(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(250),nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    post = db.Column(db.String(500), nullable=False)


class Cart(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    course_name= db.Column(db.String(250),nullable=False)
    course_code = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)

class Wishlist(db.Model):
    unique= db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    wish_list = db.Column(db.String(20), nullable=False)


class Purchase(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    course = db.Column(db.String(20), nullable=False)

class Task(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

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

@login_manager.user_loader
def load_user(id):
    if Profcontacts.query.get(int(id)): return Profcontacts.query.get(int(id))
    elif Contacts.query.get(int(id)): return Contacts.query.get(int(id))

@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')


@app.route("/courses_show", methods=['GET', 'POST'])
def Courses_show():
    r = Cart.query.filter().all()
    return render_template('courses_show.html', items=r)


@app.route("/courses", methods=['GET', 'POST'])
def courses():
    r = Cart.query.filter().all()
    wi = Wishlist.query.filter().all()
    pur = Purchase.query.filter().all()
    ids=[]
    course_ids=[]
    for i in wi:ids.append(i.user_id)
    for i in wi:
        if i.user_id == current_user.serialno:
            course_ids.append(i.wish_list)

    ids_pur = []
    course_ids_pur = []
    for i in pur: ids_pur.append(i.user)
    for i in pur:
        if i.user == current_user.serialno:
            course_ids_pur.append(i.course)
    if (request.method == 'POST'):
        q = request.form.get('type')
        w = request.form.get('wish')
        rem = request.form.get('remove')
        unen = request.form.get('unenroll')
        if rem != None:
            i,c=rem.split('-')
            entry_to_delete = Wishlist.query.filter_by(user_id=i, wish_list=c).first()
            db.session.delete(entry_to_delete)
            db.session.commit()
            return redirect('/courses')
        if w!=None and w not in course_ids:
            entry = Wishlist(user_id=current_user.serialno, wish_list=w)
            db.session.add(entry)
            db.session.commit()
            return redirect('/courses')
        if unen!=None:
            i, c = unen.split('-')
            entry_to_delete = Purchase.query.filter_by(user=i, course=c).first()
            db.session.delete(entry_to_delete)
            db.session.commit()
            return redirect('/courses')

        if q != None:
            global course_taken
            course_taken=q
            return redirect('/payment_course')
    return render_template('courses.html', items=r, wish=ids, c = course_ids, pur=pur, ids_p=ids_pur, course_ids_p=course_ids_pur)

@app.route("/payment_course", methods=['GET', 'POST'])
def payment_course():
    error = None;
    if (request.method == 'POST'):
        num = request.form.get('num')
        my = request.form.get('my')
        cvc = request.form.get('cvc')
        name = request.form.get('name')

        #verify number
        num_flag = num.isdigit() and (len(num)==6)
        my_flag = False
        if ('/' in my):
            x,y = my.split("/")
            if len(x) == len(y) and len(x) == 2 and x.isdigit() and y.isdigit():
                my_flag = True
        cvc_flag  = cvc.isdigit() and (len(cvc)==3)
        if num_flag and cvc_flag and my_flag:
            global course_taken
            print(course_taken)
            entry = Purchase(user=current_user.serialno, course=course_taken)
            db.session.add(entry)
            db.session.commit()
            course_taken=None
            return redirect('/enroll_courses')
        else:error=True
    return render_template('payment_course.html',error=error)


@app.route("/enroll_courses", methods=['GET', 'POST'])
def Enroll_courses():
    r = Cart.query.filter().all()
    wi = Wishlist.query.filter().all()
    pur = Purchase.query.filter().all()
    ids = []
    course_ids = []
    for i in wi: ids.append(i.user_id)
    for i in wi:
        if i.user_id == current_user.serialno:
            course_ids.append(i.wish_list)

    ids_pur = []
    course_ids_pur = []
    for i in pur: ids_pur.append(i.user)
    for i in pur:
        if i.user == current_user.serialno:
            course_ids_pur.append(i.course)
    if (request.method == 'POST'):
        w = request.form.get('wish')
        rem = request.form.get('remove')
        unen = request.form.get('unenroll')
        if rem != None:
            i, c = rem.split('-')
            entry_to_delete = Wishlist.query.filter_by(user_id=i, wish_list=c).first()
            db.session.delete(entry_to_delete)
            db.session.commit()
            return redirect('/enroll_courses')
        if w != None and w not in course_ids:
            entry = Wishlist(user_id=current_user.serialno, wish_list=w)
            db.session.add(entry)
            db.session.commit()
            return redirect('/enroll_courses')
        if unen != None:
            i, c = unen.split('-')
            entry_to_delete = Purchase.query.filter_by(user=i, course=c).first()
            db.session.delete(entry_to_delete)
            db.session.commit()
            return redirect('/enroll_courses')

    return render_template('enroll_courses.html', items=r, wish=ids, c=course_ids, pur=pur, ids_p=ids_pur,
                           course_ids_p=course_ids_pur)


@app.route("/wishlist", methods=['GET', 'POST'])
def Wish_list():
    r = Cart.query.filter().all()
    wi = Wishlist.query.filter().all()
    pur = Purchase.query.filter().all()
    ids = []
    course_ids = []
    for i in wi: ids.append(i.user_id)
    for i in wi:
        if i.user_id == current_user.serialno:
            course_ids.append(i.wish_list)

    ids_pur = []
    course_ids_pur = []
    for i in pur: ids_pur.append(i.user)
    for i in pur:
        if i.user == current_user.serialno:
            course_ids_pur.append(i.course)

    if (request.method == 'POST'):
        q = request.form.get('type')
        w = request.form.get('wish')
        rem = request.form.get('remove')
        unen = request.form.get('unenroll')

        if rem != None:
            i,c=rem.split('-')
            entry_to_delete = Wishlist.query.filter_by(user_id=i, wish_list=c).first()
            db.session.delete(entry_to_delete)
            db.session.commit()
            return redirect('/wishlist')

        if w!=None and w not in course_ids:
            entry = Wishlist(user_id=current_user.serialno, wish_list=w)
            db.session.add(entry)
            db.session.commit()
            return redirect('/wishlist')

        if unen != None:
            i, c = unen.split('-')
            entry_to_delete = Purchase.query.filter_by(user=i, course=c).first()
            db.session.delete(entry_to_delete)
            db.session.commit()
            return redirect('/wishlist')

        if q != None:
            global course_taken
            course_taken = q
            return redirect('/payment_course')
    return render_template('wishlist.html', items=r, wish=ids, c = course_ids,pur=pur, ids_p=ids_pur,
                           course_ids_p=course_ids_pur)




@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html')

@app.route("/professor_list")
def professor_list():
    r = Profcontacts.query.filter().all()
    return render_template('professor_list.html', result = r)



@app.route("/contact", methods = ['GET', 'POST']) #need to add more parameters for student sign up
def contact():
    try:
        if(request.method=='POST'):
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            entry = Contacts(name=name,email = email, password=password, basic_mode=1, image='https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg?20200913095930' )
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
            flash('Please fill all the field', 'danger')
            return render_template('login.html')  #need to add flash on top
        elif res[0].email==email_in and res[0].password==password_in:
            login_user(res[0])
            return redirect(url_for('user'))
        elif res[0].email==email_in and res[0].password!=password_in:
            return 'password error' #need to add flash on top

    return render_template('login.html')

@app.route("/job", methods= ['GET'])
def job(): #access database jobs
    res = Jobs.query.filter().all()
    return render_template('jobs.html', result=res)


@app.route("/scholarship", methods= ['GET'])
def scholarship(): #access database
    res = Scholarship.query.filter().all()
    return render_template('scholarship.html', result=res)

@app.route("/prof")
def prof():
    return render_template('prof.html')

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if (request.method == 'POST'):
        q = request.form.get('type')
        print(q)
        if q == "True":
            return redirect('/payment')
        else:
            current_user.basic_mode = True
        db.session.commit()
        return redirect('/profile')
    return render_template('profile.html')

@app.route("/payment", methods=['GET', 'POST'])
def payment():
    error = None;
    if (request.method == 'POST'):
        num = request.form.get('num')
        my = request.form.get('my')
        cvc = request.form.get('cvc')
        name = request.form.get('name')

        #verify number
        num_flag = num.isdigit() and (len(num)==6)
        my_flag = False
        if ('/' in my):
            x,y = my.split("/")
            if len(x) == len(y) and len(x) == 2 and x.isdigit() and y.isdigit():
                my_flag = True
        cvc_flag  = cvc.isdigit() and (len(cvc)==3)
        if num_flag and cvc_flag and my_flag:
            current_user.basic_mode = False
            db.session.commit()
            return redirect('/profile')
        else:error=True
    return render_template('payment.html',error=error)


@app.route("/jobs_user")
def jobs_user():
    res = Jobs.query.filter().all()
    return render_template('jobs_user.html', result=res)

@app.route("/scholarship_user")
def scholarship_user():
    res = Scholarship.query.filter().all()
    return render_template('scholarship_user.html', result=res)

@app.route("/professor_list_user")
def professor_list_user():
    r = Profcontacts.query.filter().all()
    return render_template('professor_list_user.html', result = r)

@app.route("/professor_profile")
def professor_profile():
    return render_template('professor_profile.html')

@app.route("/discussion", methods = ['GET', 'POST'])
def Discussion():
    ques = Query.query.filter().all()
    rep = Reply.query.filter().all()
    if (request.method == 'POST'):
        q = request.form.get('q')
        id = request.form.get('r_id')
        r = request.form.get('r')
        if q!=None and len(q) > 0:
            entry = Query(question=q, poster=current_user.name)
            db.session.add(entry)
            db.session.commit()
        elif r!=None and len(r) > 0:
            entry = Reply(r_id=id, answer=r, person=current_user.name)
            db.session.add(entry)
            db.session.commit()
        return redirect('/discussion')
    return render_template('discussion.html', ques=ques, reply=rep)


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


@app.route("/admin_login", methods= ['GET', 'POST'])
def admin_login():
    if(request.method== 'POST'):
        mail_in= request.form.get('mail')
        passw_in= request.form.get('password')
        res = Admin_login.query.filter(Admin_login.amail==mail_in).all()
        print(mail_in,passw_in,res[0].mail)
        if len(res) == 0:
            return 'error'  #need to add flash on top
        elif res[0].mail==aemail_in and res[0].apassword==passw_in:
            login_user(res[0])
            return redirect(url_for('userP'))
        elif res[0].aemail==mail_in and res[0].apassword!=passw_in:
            return 'password error' #need to add flash on top

    return render_template('admin_home.html')



@app.route('/admin_login', methods=['GET', 'POST'])
@login_required
def dashboard3():
    return render_template('admin_home.html')

@app.route('/userP', methods=['GET', 'POST'])
@login_required
def dashboard2():
    return render_template('userP.html')


@app.route('/user', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('user.html')

@app.route('/prof_post', methods=['GET', 'POST'])
def prof_post():
    if (request.method == 'POST'):
        q = request.form.get('q')
        id = request.form.get('r_id')
        if q != None and len(q) > 0:
            entry = Prof_post(post=q, name=current_user.FullName)
            db.session.add(entry)
            db.session.commit()
        return redirect('/prof_post')
    return render_template('prof_post.html', result=Prof_post.query.filter().all())

@app.route('/prof_post_offer')
def prof_post_offer():

    return render_template('prof_post_offer.html', result=Prof_post.query.filter().all())



@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/cart')
def cart():
        rows = Cart.query.filter().all()
        print(rows)
        return render_template('cart.html', carts=rows)


@app.route('/todo', methods= ['GET', 'POST'])
def todo():
    t = Task.query.filter_by(user=current_user.serialno).all()
    if (request.method == 'POST'):
        task = request.form.get('newtask')
        date_ = request.form.get('time')
        post_s = request.form.get('serial')
        clr = request.form.get('cl')
        if clr!=None:
            entries_to_delete = Task.query.filter_by(user=current_user.serialno).all()
            for entry in entries_to_delete:
                db.session.delete(entry)
            db.session.commit()
            return redirect('/todo')
        if post_s!=None:
            entry_to_delete = Task.query.filter_by(id=post_s).first()
            db.session.delete(entry_to_delete)
            db.session.commit()
            return redirect('/todo')
        if date_!=None and task!=None:
            entry = Task(user=current_user.serialno, description=task, date=date_)
            db.session.add(entry)
            db.session.commit()
            return redirect('/todo')
    return render_template('todo.html', tasks=t)



@app.route('/jobs_admin')
def jobs_admin():
    res = Jobs.query.filter().all()
    return render_template('jobs_admin.html', result=res)


@app.route('/new_jobs', methods= ['GET', 'POST'])
def new_jobs():
        res = Jobs.query.filter().all()
        if(request.method=='POST'):
            name = request.form.get('Job_Title')
            c = request.form.get('Company_Name')
            r = request.form.get('Requirement')
            l = request.form.get('Location')
            print(name,c,r,l)

            entry = Jobs(Job_Title=name,Company_Name =c , Requirement=r, Location=l )
            db.session.add(entry)
            db.session.commit()
            return render_template('jobs_admin.html', result=res)
        return render_template('new_jobs.html')





if __name__ == "__main__":
    with app.test_request_context():
        app.add_url_rule('/login.html', 'login', login)
        app.add_url_rule('/index.html', '/', home)
        app.add_url_rule('/courses.html', 'courses', courses)
        app.add_url_rule('/jobs.html', 'job', job)
        app.add_url_rule('/contact.html', 'more', contact)
        app.add_url_rule('/user.html', 'user', user)
        app.add_url_rule('/aboutus.html', 'aboutus', aboutus)
        app.add_url_rule('/scholarship.html', 'scholarship', scholarship)
        app.add_url_rule('/prof.html', 'prof', prof)
        app.add_url_rule('/userP.html', 'userP', userP)
        app.add_url_rule('/loginP.html','loginP', loginP)
        app.add_url_rule('/profcontact.html','profcontact', profcontact)
        # app.add_url_rule('/premium.html', 'premium', premium)
        app.add_url_rule('/cart.html', 'cart', cart)
        app.add_url_rule('/todo.html', 'todo', todo)


    app.run(debug=True)


#----------------------------------------------------------------



