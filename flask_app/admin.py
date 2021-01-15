from flask_app import app
from flask_app.views import *
from flask import render_template
import os

app_root = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = '\\Web Project\\Shoes Store\\app\\static\\upload'

# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('rank') != None:
        if session["rank"] == 1:
            return render_template('admin/dashboard.html', email=session["email"], name=session["name"])
    else:
        return "<script> alert('you dont have permission to access this page!!!!!!');</script> <h1>BAd Request</h1>"


@app.route("/feedbacks")
def feedbacks():
    if session.get('rank') != None:
        if session["rank"] == 1:
            myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                             app_configration["db_user_password"], app_configration["db_name"])
            contacts = myDB.show_all_contacts()
            return render_template('admin/feedbacks.html', name="Admin", contacts=contacts)

        else:
            return render_template("public/index.html")

    else:
        return render_template("public/index.html")


@app.route("/show_customer")
def show_customer():
    if session.get('rank') != None:
        if session["rank"] == 1:
            myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                             app_configration["db_user_password"], app_configration["db_name"])
            customer = myDB.show_all_customers()
            return render_template('admin/showUsers.html', name="Admin", customer=customer)

        else:
            return render_template("public/index.html")

    else:
        return render_template("public/index.html")


@app.route("/product")
def products():
    if session.get('email') != None:
        if session['rank'] == 1:
            myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                             app_configration["db_user_password"], app_configration["db_name"])
            products = myDB.get_all_products()
            print(products)
            return render_template('admin/products.html', name=session['name'], products=products)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('loginPage'))


@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if session.get('email') != None:
        if session['rank'] == 1:
            if request.method == "POST":
                name = request.form['name']
                product_desc = request.form['product_des']
                price = request.form['price']
                price = int(price)
                stock = request.form['stock']
                category=request.form['category']
                stock = int(stock)
                file = request.files['image']
                
                print(file.filename)
                target = os.path.join(app_root, r'\\Web Project\\Shoes Store\\flask_app\\static\\upload')
                print(target)
                filename = file.filename
                destination = "/".join([target, filename])
                print(destination)
                file.save(destination)
                myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                                 app_configration["db_user_password"], app_configration["db_name"])
                if myDB.add_new_product(name, product_desc, file.filename, stock, price,category):
                    products = myDB.get_all_products()
                    print(products)
                    return render_template('admin/products.html', name=session['name'], products=products)
                else:
                    return redirect(request.url)
            else:
                return render_template('admin/add_products.html', name=session['name'])

        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('loginPage'))


@app.route("/delete_product")
def delete_product():
    args = request.args
    prod_id = args.get('id')

    if id:
        myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                         app_configration["db_user_password"], app_configration["db_name"])
        if myDB.delete_product(prod_id):
            return redirect(url_for("products"))
        else:
            return redirect(request.url)
    else:
        return render_template('admin/dashboard.html', name=session['name'])


@app.route("/orders", methods=["POST", "GET"])
def orders():
    if session.get('email')!=None:
        if session['rank']==1:
            myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                         app_configration["db_user_password"], app_configration["db_name"])
            orders=myDB.get_order()
            return render_template("admin/orders.html", name=session['name'],orders=orders)
        else:
            return redirect( url_for( 'loginPage' ) )
    else:
        return redirect( url_for( 'loginPage' ) )
    
    
@app.route("/sales", methods=["POST", "GET"])
def sales():
    if session.get('email')!=None:
        if session['rank']==1:
            myDB = DBHandler(app_configration["host"], app_configration["db_user_name"],
                         app_configration["db_user_password"], app_configration["db_name"])
            # orders=myDB.get_order()
            total_sales=myDB.get_sales()
            profit=myDB.get_profit()
            return render_template("admin/sales.html", name=session['name'],total_sales=total_sales,profit=profit)
        else:
            return redirect( url_for( 'loginPage' ) )
    else:
        return redirect( url_for( 'loginPage' ) )
            