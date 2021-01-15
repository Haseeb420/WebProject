from flask_app import app
from flask import render_template, request, session, redirect, url_for, jsonify
from flask_app.DBHandler import DBHandler
from flask_app.config import *
from flask_mail import Mail, Message
import smtplib
import random
# from flask_sqlalchemy import SQLAlchemy

# app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:@localhost/test"
# db=SQLAlchemy(app)

app.config["SECRET_KEY"] = app_configration["secret_key"]
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = app_configration['email_user']
app.config['MAIL_PASSWORD'] = app_configration['email_user_password']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/")
@app.route("/home")
def home():
    myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                     app_configration["db_user_password"], app_configration["db_name"])
    products = myDB.get_all_products()
    category = myDB.get_categories()
    if session.get('rank') != None:
        if session['rank'] == 2:
            return render_template("public/index.html", name=session['name'], category=category, products=products)
        else:
            return render_template("public/login.html")

    else:
        myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                         app_configration["db_user_password"], app_configration["db_name"])
        products = myDB.get_all_products()
        print(products)
        return render_template("public/index.html", category=category, products=products)


@app.route('/about')
def about():
    if session.get('rank') != None:
        if session['rank'] == 2:
            return render_template('public/about.html', name=session['name'])

    return render_template('public/about.html')


@app.route('/contact')
def contact():
    if session.get('rank') != None:
        if session['rank'] == 2:
            return render_template("public/contact.html", name=session['name'])
    else:
        return render_template('public/contact.html',)


@app.route("/login")
def loginPage():
    return render_template('public/login.html')


@app.route("/signUp", methods=["POST", "GET"])
def signUp():
    if request.method == "POST":
        form = request.form
        fname = form['fname']
        lname = form['lname']
        email = form['email']
        phone = form['phone']
        password = form['password']

        full_name = fname+" "+lname
        myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                         app_configration["db_user_password"], app_configration["db_name"])

        if myDB.add_new_user(full_name, email, phone, password):
            sub = "Welcome to Online Shoes Store"
            msg = Message(sub, sender=app_configration['email_user'],
                          recipients=[email])

            msg.body = """Hello {}! \n Welcome to Online Shoes Store\n Thanks for Joining us.\n 
            Regards \n Online Shoes Store""".format(full_name)

            mail.send(msg)

            data = myDB.get_data(email)
            data = data[0]

            session['id'] = data["id"]
            session["name"] = data["name"]
            session["email"] = data["email"]
            session["phone"] = data["phone"]
            session["password"] = data["password"]
            session['rank'] = data["rank"]

            if session['rank'] == 1:
                return render_template('admin/dashboard.html', name=session["name"], email=email)
            elif session['rank'] == 2:

                return redirect(url_for("home"))
        else:
            return redirect(url_for("signUp"))
    else:
        return render_template('public/signUp.html')


@app.route("/login_data", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form['username']
        password = request.form['password']
        myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                         app_configration["db_user_password"], app_configration["db_name"])
        if myDB.login(email, password):
            data = myDB.get_data(email)
            data = data[0]
            session['id'] = data["id"]
            session["name"] = data["name"]
            session["email"] = data["email"]
            session["phone"] = data["phone"]
            session["password"] = data["password"]
            session['rank'] = data["rank"]
            if session['rank'] == 1:
                return render_template('admin/dashboard.html', name=session['name'], email=session['email'])
            elif session['rank'] == 2:
                return redirect(url_for('home'))

        else:
            return redirect(url_for('loginPage'))

    else:

        return redirect(url_for('loginPage'))


@app.route('/profile')
def profile():
    if session.get('email') != None:
        myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                         app_configration["db_user_password"], app_configration["db_name"])
        if session['email']:
            data = myDB.get_data(session["email"])
            data = data[0]
            if session['rank'] == 1:
                return render_template("admin/profile.html", name=session['name'], data=data)
            else:
                return render_template("public/profile.html", name=session['name'], data=data)
        else:
            return redirect(url_for('loginPage'))

    else:
        return redirect(url_for('loginPage'))


@app.route('/change_profile')
def change_profile():
    if session.get('email') != None:
        if request.method == "POST":
            jsonobj = request.get_json()

            myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                             app_configration["db_user_password"], app_configration["db_name"])

            return render_template("admin/profile.html", name="Admin", data=data)

        else:
            return render_template("public/profile.html")

    else:
        return redirect(url_for('loginPage'))


@app.route('/contact_us', methods=["POST", "GET"])
def contact_us():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["Email"]
        subject = request.form["subject"]
        content = request.form["content"]
        myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                         app_configration["db_user_password"], app_configration["db_name"])
        if myDB.contact_us(name, email, subject, content):
            msg = "Your has been send....."
            return render_template('contact.html', msg=msg)
        else:
            error_msg = "Your feedback not send....."
            return render_template('public/contact.html', error_msg=error_msg)
    else:
        error_msg = "Your feedback not send....."
        return render_template('public/contact.html', error_msg=error_msg,)


@app.route('/change_password', methods=["POST", "GET"])
def change_password():
    if session.get('id') != None:
        if session['rank'] == 1:
            return render_template('admin/changePassword.html', name=session['name'])
        else:
            return render_template('public/changePassword.html', name=session['name'])
    else:
        return redirect(url_for('loginPage'))

@app.route('/forgot_password', methods=["POST", "GET"])
def forgot_password():
    return render_template('public/forgotPassword.html')    


@app.route('/forgot_password/verification', methods=["POST", "GET"])
def forgot_password_verification():
    if request.method == "POST":
            jsonobj = request.get_json()
            email = jsonobj["email"]
            myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                             app_configration["db_user_password"], app_configration["db_name"])
            
            dic={}
            if myDB.check_email_uniqueness(email):
                data=myDB.get_data(email)
                
                if data:
                    data=data[0]
                    password = data["password"]
                    name = data["name"]
                    sub = "Yuor Password"
                    msg = Message(sub, sender=app_configration['email_user'],recipients=[email])

                    msg.body = """Hello {}!
                    \nYoue new password is {}
                    Thanks for Placing this order us.\n 
                    Regards \n Online Shoes Store""".format(name,password)
                    mail.send(msg)         
                    dic["msg"]="your password will be send on your email"
            
            else:
                dic["error_msg"]="email not exist...."
            
                
         
            return jsonify(dic)
    else:
        return render_template('public/forgotPassword.html')    


@app.route('/change_password/change', methods=["POST"])
def change_password_change():
    if session.get('id') != None:
        if request.method == "POST":
            jsonobj = request.get_json()
            current_password = jsonobj["current_password"]
            new_password = jsonobj["new_password"]
            print(new_password)
            confirm_password = jsonobj["confirm_password"]
            dic = {}
            if current_password != session["password"]:
                dic["password_error"] = "current password dont't match"
                if new_password != confirm_password:
                    dic["match_error"] = "please confirm your new password"
                return jsonify(dic)
            elif new_password != confirm_password:
                dic["match_error"] = "please confirm your new password"
                return jsonify(dic)
            else:
                myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                                 app_configration["db_user_password"], app_configration["db_name"])
                if myDB.change_password(session['id'], new_password):
                    dic["success_msg"] = "Password SucessFully Change..."
                    return jsonify(dic)
                else:
                    return jsonify(dic)
        else:
            render_template('admin/changePassword.html', name="Admin")
    else:
        return redirect(url_for('loginPage'))


@app.route('/check_email', methods=["POST"])
def check_email():
    if request.method == "POST":
        jsonobj = request.get_json()
        print(jsonobj)
        email = jsonobj["email"]
        print(email)
        dic = {}
        myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                         app_configration["db_user_password"], app_configration["db_name"])
        if myDB.check_email_uniqueness(email):
            dic["not_unique"] = "Email Already Exist"
            return jsonify(dic)
        else:
            return jsonify(dic)

    else:
        redirect(url_for(signUp))


@app.route('/check_phone', methods=["POST"])
def check_phone():
    if request.method == "POST":
        jsonobj = request.get_json()
        print(jsonobj)
        phone = jsonobj["phone"]
        print(phone)
        dic = {}
        myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                         app_configration["db_user_password"], app_configration["db_name"])
        if myDB.check_phone_uniqueness(phone):
            dic["phone_unique"] = "Phone Already Exist"
            return jsonify(dic)
        else:
            return jsonify(dic)

    else:
        redirect(url_for(signUp))


@app.route('/add_to_cart', methods=["POST", "GET"])
def add_to_cart():
    if session.get('email') != None:
        args = request.args
        prod_id = args.get('id')

        if prod_id:
            myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                             app_configration["db_user_password"], app_configration["db_name"])
            product = myDB.select_product_by_id(prod_id)
            product = product[0]
            if request.method == "POST":
                form = request.form
                province = form['province']
                city = form['city']
                town = form['town']
                address = form['address']
                shipping_fee = form['shipping_fee']
                total = form['total']
                if myDB.add_to_cart(session['id'], province, city, town, address, prod_id, product.prod_price, shipping_fee, total):
                    sub = "Thanks for placing Order"
                    msg = Message(sub, sender=app_configration['email_user'],
                                  recipients=[session['email']])

                    msg.body = """Hello {}! \n Thanks for Placing this order us.\n 
                    Regards \n Online Shoes Store""".format(session['name'])
                    mail.send(msg)
                    new_stock = product.stock-1
                    stock = myDB.get_stock(prod_id)
                    if stock < 25:
                        sub = "Update Product Stock"
                        msg = Message(sub, sender=app_configration['email_user'],
                                      recipients=[app_configration["admin_mail"]])
                        msg.body = """Hello {}! you product with id {} is out of stock please update your stock\n Thanks for Placing this order us.\n 
                        Regards \n Online Shoes Store""".format(session['name'])
                        mail.send(msg)
                    myDB.decrese_stock("Admin", prod_id)
                    return redirect(url_for('home'))

            else:
                return render_template('public/addtocart.html', name=session['name'], product=product)
        else:
            return "add to cart"
    else:
        return redirect(url_for('loginPage'))


@app.route('/update_profile', methods=["POST", "GET"])
def update_profile():
    if session.get('email') != None:
        if session["email"]:
            myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                             app_configration["db_user_password"], app_configration["db_name"])
            if request.method == "POST":
                form = request.form
                name = form['name']
                email = form['email']
                phone = form['phone']
                if myDB.update_profile(session['id'], name, email, phone):
                    data = myDB.get_data(email)
                    data = data[0]
                    session['id'] = data["id"]
                    session["name"] = data["name"]
                    session["email"] = data["email"]
                    session["phone"] = data["phone"]
                    session["password"] = data["password"]
                    session['rank'] = data["rank"]
                    return redirect(url_for('profile'))
                else:
                    return redirect(url_for('profile'))

            else:
                return redirect(url_for('profile'))
    else:
        return redirect(url_for('loginPage'))


@app.route('/logout')
def logout():
    if session.get('email') != None:
        if session["email"]:
            session.clear()
            return redirect(url_for('home'))
        else:
            return redirect(url_for('loginPage'))
    else:
        return redirect(url_for('loginPage'))
