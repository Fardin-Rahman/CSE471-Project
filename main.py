from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql
import datetime
pymysql.install_as_MySQLdb()
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask import flash, session, render_template, request, redirect, url_for
import os
from datetime import date

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


@app.route("/courses", methods=['GET', 'POST'])
def courses():
    r = Cart.query.filter().all()
    wi = Wishlist.query.filter().all()
    ids=[]
    course_ids=[]
    for i in wi:ids.append(i.user_id)
    for i in wi:
        if i.user_id == current_user.serialno:
            course_ids.append(i.wish_list)

    if (request.method == 'POST'):
        q = request.form.get('type')
        w = request.form.get('wish')
        rem = request.form.get('remove')

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

        if q == 'True':
            return redirect('/payment_course')
        db.session.commit()
        return redirect('/courses')
    return render_template('courses.html', items=r, wish=ids, c = course_ids)

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
            current_user.basic_mode = False
            db.session.commit()
            return redirect('/courses')
        else:error=True
    return render_template('payment_course.html',error=error)




@app.route("/wishlist", methods=['GET', 'POST'])
def Wish_list():
    r = Cart.query.filter().all()
    wi = Wishlist.query.filter().all()
    ids=[]
    course_ids=[]
    for i in wi:ids.append(i.user_id)
    for i in wi:
        if i.user_id == current_user.serialno:
            course_ids.append(i.wish_list)

    if (request.method == 'POST'):
        q = request.form.get('type')
        w = request.form.get('wish')
        rem = request.form.get('remove')

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

        if q == 'True':
            return redirect('/payment_course')
        db.session.commit()
        return redirect('/wishlist')
    return render_template('wishlist.html', items=r, wish=ids, c = course_ids)




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


# @app.route('/premium')
# def premium():
#     courses = Premium.query.all()
#     total_courses_in_cart = sum(1 for course in courses if course.cart == CartStatus.yes)
#     return render_template('premium.html', courses=courses, total_courses_in_cart=total_courses_in_cart)
#
#
# @app.route('/add_course', methods=['POST'])
# def add_course():
#     course_name = request.form['course_name']
#     wishlist_status = request.form.get('wishlist', 'no')
#     cart_status = request.form.get('cart', 'no')
#
#     wishlist_status = WishlistStatus.yes if wishlist_status == 'yes' else WishlistStatus.no
#     cart_status = CartStatus.yes if cart_status == 'yes' else CartStatus.no
#
#     course = Premium(c_name=course_name, wishlist=wishlist_status, cart=cart_status)
#     db.session.add(course)
#     db.session.commit()
#
#     return "Juha edited successfully."
#
#
# @app.route('/add', methods=['POST'])
# def add_product_to_cart():
#     cursor = None
#     try:
#         _quantity = int(request.form['quantity'])
#         _code = request.form['code']
#         # validate the received values
#         if _quantity and _code and request.method == 'POST':
#             conn = db.connect()
#             cursor = conn.cursor(pymysql.cursors.DictCursor)
#             cursor.execute("SELECT * FROM cart WHERE code=%s", _code)
#             row = cursor.fetchone()
#
#             itemArray = {row['code']: {'course_name': row['course_name'], 'course_code': row['coursecode'],
#                                        'quantity': _quantity, 'price': row['price'], 'image': row['image'],
#                                        'total_price': _quantity * row['price']}}
#
#             all_total_price = 0
#             all_total_quantity = 0
#
#             session.modified = True
#             if 'cart_item' in session:
#                 if row['course_code'] in session['cart_item']:
#                     for key, value in session['cart_item'].items():
#                         if row['course_code'] == key:
#                             # session.modified = True
#                             # if session['cart_item'][key]['quantity'] is not None:
#                             #    session['cart_item'][key]['quantity'] = 0
#                             old_quantity = session['cart_item'][key]['quantity']
#                             total_quantity = old_quantity + _quantity
#                             session['cart_item'][key]['quantity'] = total_quantity
#                             session['cart_item'][key]['total_price'] = total_quantity * row['price']
#                 else:
#                     session['cart_item'] = array_merge(session['cart_item'], itemArray)
#
#                 for key, value in session['cart_item'].items():
#                     individual_quantity = int(session['cart_item'][key]['quantity'])
#                     individual_price = float(session['cart_item'][key]['total_price'])
#                     all_total_quantity = all_total_quantity + individual_quantity
#                     all_total_price = all_total_price + individual_price
#             else:
#                 session['cart_item'] = itemArray
#                 all_total_quantity = all_total_quantity + _quantity
#                 all_total_price = all_total_price + _quantity * row['price']
#
#             session['all_total_quantity'] = all_total_quantity
#             session['all_total_price'] = all_total_price
#
#             return redirect(url_for('.cart'))
#         else:
#             return 'Error while adding item to cart'
#     except Exception as e:
#         print(e)
#     finally:
#         cursor.close()
#         conn.close()


@app.route('/cart')
def cart():
        rows = Cart.query.filter().all()
        print(rows)
        return render_template('cart.html', carts=rows)



# @app.route('/empty')
# def empty_cart():
#     try:
#         session.clear()
#         return redirect(url_for('.cart'))
#     except Exception as e:
#         print(e)
#
#
# @app.route('/delete/<string:code>')
# def delete_product(code):
#     try:
#         all_total_price = 0
#         all_total_quantity = 0
#         session.modified = True
#
#         for item in session['cart_item'].items():
#             if item[0] == code:
#                 session['cart_item'].pop(item[0], None)
#                 if 'cart_item' in session:
#                     for key, value in session['cart_item'].items():
#                         individual_quantity = int(session['cart_item'][key]['quantity'])
#                         individual_price = float(session['cart_item'][key]['total_price'])
#                         all_total_quantity = all_total_quantity + individual_quantity
#                         all_total_price = all_total_price + individual_price
#                 break
#
#         if all_total_quantity == 0:
#             session.clear()
#         else:
#             session['all_total_quantity'] = all_total_quantity
#             session['all_total_price'] = all_total_price
#
#         # return redirect('/')
#         return redirect(url_for('.cart'))
#     except Exception as e:
#         print(e)
#
#
# def array_merge(first_array, second_array):
#     if isinstance(first_array, list) and isinstance(second_array, list):
#         return first_array + second_array
#     elif isinstance(first_array, dict) and isinstance(second_array, dict):
#         return dict(list(first_array.items()) + list(second_array.items()))
#     elif isinstance(first_array, set) and isinstance(second_array, set):
#         return first_array.union(second_array)
#     return False
#
# #### If this file doesn't exist, create it
# if 'tasks.txt' not in os.listdir('.'):
#     with open('tasks.txt','w') as f:
#         f.write('')
#
#
# def gettasklist():
#     with open('tasks.txt','r') as f:
#         tasklist = f.readlines()
#     return tasklist
#
# def createnewtasklist():
#     os.remove('tasks.txt')
#     with open('tasks.txt','w') as f:
#         f.write('')
#
# def updatetasklist(tasklist):
#     os.remove('tasks.txt')
#     with open('tasks.txt','w') as f:
#         f.writelines(tasklist)
#
#
#
'''
@app.route('/')
def todo():
    return render_template('todo.html', datetoday2=datetoday2, tasklist=gettasklist(), l=len(gettasklist()))



@app.route('/clear')
def clear_list():
    createnewtasklist()
    return render_template('todo.html', datetoday2=datetoday2, tasklist=gettasklist(), l=len(gettasklist()))
'''
#

# @app.route('/addtask', methods=['POST'])
# def add_task():
#     task = request.form.get('newtask')
#     with open('tasks.txt', 'a') as f:
#         f.writelines(task + '\n')
#     return render_template('todo.html', datetoday2=datetoday2, tasklist=gettasklist(), l=len(gettasklist()))
#
#
#
# @app.route('/deltask', methods=['GET'])
# def remove_task():
#     task_index = int(request.args.get('deltaskid'))
#     tasklist = gettasklist()
#     print(task_index)
#     print(tasklist)
#     if task_index < 0 or task_index > len(tasklist):
#         return render_template('todo.html', datetoday2=datetoday2, tasklist=tasklist, l=len(tasklist),
#                                mess='Invalid Index...')
#     else:
#         removed_task = tasklist.pop(task_index)
#     updatetasklist(tasklist)
#     return render_template('todo.html', datetoday2=datetoday2, tasklist=tasklist, l=len(tasklist))


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
        # app.add_url_rule('/todo.html', 'todo', todo)


    app.run(debug=True)


#----------------------------------------------------------------



