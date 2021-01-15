from flask_app.User import User
import pymysql
from flask_app.Product import Product
from flask_app.Order import Order


class DBHandler:
    def __init__(self, host, db_user, db_pswd, db_name):
        self.host = host
        self.db_user = db_user
        self.db_pswd = db_pswd
        self.db_name = db_name
        self.user = User()

    def login(self, email, password):
        mydb = None
        login_flag = False
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = "select * from users where user_email=%s and password=%s"
            argumnets = (email, password)
            mydb_cursor.execute(sql, argumnets)
            data = mydb_cursor.fetchone()
            if data:
                self.user.id = data[0]
                self.user.name = data[1]
                self.user.email = data[2]
                self.user.password = [3]
                self.user.rank = data[4]
                login_flag = True

        except Exception as E:
            print(str(E))
            return login_flag

        finally:
            if mydb != None:
                mydb.close()
                return login_flag

    def gett_rank(self, email):
        mydb = None
        rank = 0
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = "select * from users where user_email=%s"
            argumnets = (email)
            mydb_cursor.execute(sql, argumnets)
            data = mydb_cursor.fetchone()
            if data:
                rank = data[5]

        except Exception as E:
            print(str(E))
            return rank

        finally:
            if mydb != None:
                mydb.close()
                return rank

    def get_id(self):
        return self.user.id

    def get_id(self):
        return self.user.id

    def contact_us(self, name, email, subject, msg):
        mydb = None
        contact_us_flag = False
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = "insert into contact (user_name,user_email,subject,content) values (%s,%s,%s,%s)"
            argumnets = (name, email, subject, msg)
            mydb_cursor.execute(sql, argumnets)
            mydb.commit()
            contact_us_flag = True

        except Exception as E:
            print(str(E))
            return contact_us_flag

        finally:
            if mydb != None:
                mydb.close()
                return contact_us_flag

    def get_data(self, email):
        mydb = None
        data_list = []
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = "select * from users where user_email=%s "
            argumnets = (email)
            mydb_cursor.execute(sql, argumnets)
            data = mydb_cursor.fetchone()
            data_list.append({
                'id': data[0],
                'name': data[1],
                'email': data[2],
                'phone': data[3],
                'password': data[4],
                'rank': data[5]
            })
        except Exception as E:
            print(str(E))
            return data_list
        finally:
            if mydb != None:
                mydb.close()
                return data_list

    def show_all_contacts(self):
        mydb = None
        contacts_list = []
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = "select * from  contact"
            mydb_cursor.execute(sql)
            contacts = mydb_cursor.fetchall()
            print(contacts)
            if contacts:
                for x in contacts:
                    print(x[0])
                    print(x[1])
                    print(x[2])
                    print(x[3])
                    print(x[4])
                    contacts_list.append({
                        "id": x[0],
                        "name": x[1],
                        "email": x[2],
                        "subject": x[3],
                        "content": x[4]
                    })

        except Exception as E:
            print(str(E))
            return contacts_list

        finally:
            if mydb != None:
                mydb.close()
                print(contacts_list)
                return contacts_list

    def change_password(self, id, password):
        mydb = None
        change_password_flag = False
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = "UPDATE users SET password = %s WHERE users.user_id =%s ;"
            argumnets = (password, id)
            mydb_cursor.execute(sql, argumnets)
            mydb.commit()
            change_password_flag = True

        except Exception as E:
            print(str(E))
            return change_password_flag
        finally:
            if mydb != None:
                mydb.close()
                return change_password_flag

    def update_profile(self, id, name, email, phone):
        mydb = None
        update_flag = False
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = "UPDATE users SET user_name = %s,user_email=%s,user_phone=%s WHERE users.user_id =%s ;"
            argumnets = (name, email, phone, id)
            mydb_cursor.execute(sql, argumnets)
            mydb.commit()
            update_flag = True

        except Exception as E:
            print(str(E))
            return update_flag
        finally:
            if mydb != None:
                mydb.close()
                return update_flag

    def get_all_products(self):
        mydb = None
        products = []
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = "select * from product;"
            mydb_cursor.execute(sql)
            data = mydb_cursor.fetchall()
            if data:
                for x in data:
                    products.append(
                        Product(x[0], x[1], x[2], x[3], x[4], x[5]))

            print(products)
        except Exception as E:
            print(str(E))
            return products
        finally:
            if mydb != None:
                mydb.close()
                return products

    def check_email_uniqueness(self, email):
        mydb = None
        email_exist = False
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = "select * from users where user_email=%s"
            argumnets = (email)
            mydb_cursor.execute(sql, argumnets)
            data = mydb_cursor.fetchone()
            if data:
                email_exist = True
                for d in data:
                    print(d)

        except Exception as E:
            print(str(E))
            return email_exist

        finally:
            if mydb != None:
                mydb.close()
                return email_exist

    def check_phone_uniqueness(self, phone):
        mydb = None
        phone_exist = False
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = "select * from users where user_phone=%s"
            argumnets = (phone)
            mydb_cursor.execute(sql, argumnets)
            data = mydb_cursor.fetchone()
            if data:
                phone_exist = True
                for d in data:
                    print(d)

        except Exception as E:
            print(str(E))
            return phone_exist

        finally:
            if mydb != None:
                mydb.close()
                return phone_exist

    def add_new_user(self, name, email, phone, password):
        mydb = None
        add_new_user_flag = False
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = " INSERT INTO USERS ( user_name , user_email , user_phone , password, rank  ) VALUES ( %s , %s , %s , %s , %s );"
            argumnets = (name, email, phone, password, 2)
            mydb_cursor.execute(sql, argumnets)
            mydb.commit()
            add_new_user_flag = True

        except Exception as E:
            print(str(E))
            return add_new_user_flag
        finally:
            if mydb != None:
                mydb.close()
                return add_new_user_flag

    def show_all_customers(self):
        mydb = None
        contacts_list = []
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = "select * from  users where rank=2"
            mydb_cursor.execute(sql)
            contacts = mydb_cursor.fetchall()
            print(contacts)
            if contacts:
                for x in contacts:
                    contacts_list.append(
                        User(x[0], x[1], x[2], x[3], x[4], x[5]))

        except Exception as E:
            print(str(E))
            return contacts_list

        finally:
            if mydb != None:
                mydb.close()
                print(contacts_list)
                return contacts_list

    def add_new_product(self, p_name, product_desc, product_img, product_stock, product_price, category):
        mydb = None
        add_new_product_flag = False
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = """ INSERT INTO PRODUCT (product_name, product_des, product_img, product_stock,
            product_price, category  ) VALUES ( %s , %s , %s , %s , %s ,%s);"""
            argumnets = (p_name, product_desc, product_img,
                         product_stock, product_price, category)
            mydb_cursor.execute(sql, argumnets)
            mydb.commit()
            add_new_product_flag = True

        except Exception as E:
            print(str(E))
            return add_new_product_flag
        finally:
            if mydb != None:
                mydb.close()
                return add_new_product_flag

    def delete_product(self, prod_id):
        mydb = None
        delete_product_flag = False
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = " DELETE FROM PRODUCT WHERE product_id=%s"
            argumnets = (prod_id)
            mydb_cursor.execute(sql, argumnets)
            mydb.commit()
            delete_product_flag = True

        except Exception as E:
            print(str(E))
            return delete_product_flag
        finally:
            if mydb != None:
                mydb.close()
                return delete_product_flag

    def select_product_by_id(self, prod_id):
        mydb = None
        products = []
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = "select * from product where product_id=%s;"
            arg = (prod_id)
            mydb_cursor.execute(sql, arg)
            data = mydb_cursor.fetchall()
            if data:
                for x in data:
                    print(x)
                    products.append(
                        Product(x[0], x[1], x[2], x[3], x[4], x[5]))
        except Exception as E:
            print(str(E))
            return products
        finally:
            if mydb != None:
                mydb.close()
                return products

    def get_categories(self):
        mydb = None
        categories = []
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = "SELECT DISTINCT(category) from product"
            mydb_cursor.execute(sql)
            data = mydb_cursor.fetchall()
            if data:
                for x in data:
                    categories.append(x[0])
                    print(x[0])

            print(categories)
        except Exception as E:
            print(str(E))
            return categories
        finally:
            if mydb != None:
                mydb.close()
                return categories

    def add_to_cart(self, user_id, province, city, town, address, prod_id, price, shipping_fee, total):
        mydb = None
        add_new_product_flag = False
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = """INSERT INTO `orders`(user_id,`Province`, `City`, `Town`, `Address`, `product_id`, `product_price`, `shipping fee`, `Total`) 
                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            argumnets = (user_id, province, city, town, address,
                         prod_id, price, shipping_fee, total)
            mydb_cursor.execute(sql, argumnets)
            mydb.commit()
            add_new_product_flag = True

        except Exception as E:
            print(str(E))
            return add_new_product_flag
        finally:
            if mydb != None:
                mydb.close()
                return add_new_product_flag

    def decrese_stock(self, prod_id, new_stock):
        mydb = None
        delete_product_flag = False
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = "UPDATE `product` SET `product_stock`=%s WHERE 'product_id'=%s"
            argumnets = (prod_id, new_stock)
            mydb_cursor.execute(sql, argumnets)
            mydb.commit()
            delete_product_flag = True

        except Exception as E:
            print(str(E))
            return delete_product_flag
        finally:
            if mydb != None:
                mydb.close()
                return delete_product_flag

    def get_stock(self, prod_id):
        mydb = None
        product_stock = 0
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = "SELECT product_stock FROM `product` WHERE product_id=%s "
            argumnets = (prod_id)
            mydb_cursor.execute(sql, argumnets)
            data = mydb_cursor.fetchone()
            if data:
                product_stock=data[0][0]

        except Exception as E:
            print(str(E))
            return product_stock
        finally:
            if mydb != None:
                mydb.close()
                return product_stock

    def get_order(self):
        mydb = None
        products = []
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = "select * from orders order by date desc;"
            mydb_cursor.execute(sql)
            data = mydb_cursor.fetchall()
            if data:
                for x in data:
                    print(x)
                    products.append(
                        Order(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10]))
        except Exception as E:
            print(str(E))
            return products
        finally:
            if mydb != None:
                mydb.close()
                return products

    def get_sales(self):
        mydb = None
        sales = 0
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = "select sum(total)from orders;"
            mydb_cursor.execute(sql)
            data = mydb_cursor.fetchone()
            if data:
                sales = data[0]
        except Exception as E:
            print(str(E))
            return sales
        finally:
            if mydb != None:
                mydb.close()
                return sales

    def get_profit(self):
        mydb = None
        profit = 0
        try:
            mydb = pymysql.connect(
                self.host, self.db_user, self.db_pswd, self.db_name)
            mydb_cursor = mydb.cursor()
            sql = "SELECT sum(product_price-(product_price-(product_price/100*10))) from orders;"
            mydb_cursor.execute(sql)
            data = mydb_cursor.fetchone()
            if data:
                profit = data[0]
        except Exception as E:
            print(str(E))
            return profit
        finally:
            if mydb != None:
                mydb.close()
                return profit
