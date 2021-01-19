#!C:\Python39\python.exe -T

from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta
import datetime
import pymysql
import bcrypt
import re

app = Flask(__name__)
app.secret_key = "123"
app.permanent_session_lifetime = timedelta(hours=24)

message = ""
now = datetime.datetime.now()

@app.route("/")
def index():
    return render_template("index.html", site="index")

@app.route("/szolgaltatasok")
def szolgaltatasok():
    conn = pymysql.connect(host="localhost", user="root", passwd="", database="computerdesk")
    cursor = conn.cursor(pymysql.cursors.DictCursor)


    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    return render_template("products.html", products=rows, site="products")

@app.route("/rolunk")
def rolunk():
    return render_template("us.html", site="us")

@app.route("/elerhetosegek")
def elerhetosegek():
    return render_template("contact.html", site="support")

@app.route("/kosar")
def kosar():
    return render_template("cart.html", site="cart")


#  Cart

@app.route("/add_inc", methods=["POST", "GET"])
def add_inc():

    form_data = request.form

    quantity = int(form_data["quantity"])
    product_code = form_data["code"]

    if quantity and product_code and request.method == "POST":
        conn = pymysql.connect(host="localhost", user="root", passwd="", database="computerdesk")
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM products WHERE code=%s", product_code)
        row = cursor.fetchone()
        
        itemArray = { row['code'] : {'id' : row['id'], 'code' : row['code'],  'name' : row['name'], 'quantity' : quantity, 'price' : row['price'], 'icon' : row['icon'], 'total_price': quantity * row['price']}}

        all_total_quantity = 0
        all_total_price = 0
        session.modified = True

        if "cartItems" in session:
            if row["code"] in session["cartItems"]:
                for key, value in session["cartItems"].items():
                    if row["code"] == key:
                        old_quantity = session["cartItems"][key]["quantity"]
                        total_quantity = old_quantity + quantity
                        session["cartItems"][key]["quantity"] = total_quantity
                        session["cartItems"][key]["total_price"] = total_quantity * row["price"]
                        all_total_quantity = all_total_quantity + quantity
                        all_total_price = all_total_price

            else:
                session["cartItems"].update(itemArray)
            
            for key, value in session["cartItems"].items():
                individual_quantity = int(session["cartItems"][key]["quantity"])
                individual_price = int(session["cartItems"][key]["total_price"])
                all_total_quantity = all_total_quantity + individual_quantity
                all_total_price = all_total_price + individual_price

        else:
            session["cartItems"] = itemArray
            all_total_quantity = all_total_quantity + quantity
            all_total_price = all_total_quantity * row["price"]
        
        session["all_total_quantity"] = all_total_quantity
        session["all_total_price"] = all_total_price

        return redirect(url_for(".szolgaltatasok", message="sikeres-kosarhoz-adas"))
    
    else:
        return redirect(url_for(".szolgaltatasok", message="sikertelen-kosarhoz-adas"))

@app.route("/empty_cart_inc", methods=["POST", "GET"])
def empty_cart_inc():
    session.pop("cartItems", None)
    return redirect(url_for(".kosar", message="sikeres-urites"))

@app.route("/delete_product_cart_inc/", methods=["POST", "GET"])
def delete_product_cart_inc():

    code = request.args.get("code")

    all_total_price = 0
    all_total_quantity = 0
    session.modified = True

    for item in session["cartItems"].items():
        if item[0] == code:
            session["cartItems"].pop(item[0], None)
            if "cartItems" in session:
                for key, value in session["cartItems"].items():
                    individual_quantity = int(session["cartItems"][key]["quantity"])
                    individual_price = int(session["cartItems"][key]["total_price"])
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price
                break

    if all_total_quantity == 0:
        session.pop("cartItems", None)

    else:
        session["all_total_quantity"] = all_total_quantity
        session["all_total_price"] = all_total_price
    
    if "cartItems" in session:
        message = "sikeres-torles"
    else:
        message = "sikeres-urites"
    
    return redirect(url_for(".kosar", message=message))

@app.route("/add_product_inc", methods=["GET", "POST"])
def add_product_inc():

    conn = pymysql.connect(host="localhost", user="root", passwd="", database="computerdesk")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    form_data = request.args

    if request.method == "GET":
        cursor.execute("INSERT INTO products (code, name, icon, price) VALUES (%s, %s, %s, %s)", (form_data["code"], form_data["name"], form_data["icon"], form_data["price"]))
        conn.commit()
        return redirect(url_for(".fiok", message="sikeres-termek-letrehozas"))
    else:
        return redirect(url_for(".fiok", message="sikertelen-termek-letrehozas"))

@app.route("/delete_product_inc")
def delete_product_inc():

    conn = pymysql.connect(host="localhost", user="root", passwd="", database="computerdesk")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    form_data = request.args

    if form_data["name"]:
        cursor.execute("DELETE FROM products WHERE name=%s", (form_data["name"]))
        conn.commit()
        return redirect(url_for(".fiok", message="sikeres-termek-torles"))
    else:
        return redirect(url_for(".fiok", message="sikertelen-termek-torles"))

@app.route("/update_product_inc")
def update_product_inc():

    conn = pymysql.connect(host="localhost", user="root", passwd="", database="computerdesk")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    form_data = request.args

    cursor.execute("UPDATE products SET name=%s, icon=%s, price=%s WHERE id=%s", (form_data["name"], form_data["icon"], form_data["price"], form_data["id"]))
    conn.commit()
    return redirect(url_for(".fiok", message="sikeres-termek-frissites"))


#  Account 


@app.route("/login_inc", methods=["POST", "GET"])
def login_inc():

    # Database connection
    conn = pymysql.connect(host="localhost", user="root", passwd="", database="computerdesk")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    form_data = request.form

    cursor.execute("SELECT * FROM users WHERE usersUid = %s", (form_data["uid"]))
    account = cursor.fetchone()

    valid = bcrypt.checkpw(form_data["pwd"].encode("utf-8"), account["usersPwd"].encode("utf-8"))

    if account and valid:

        if form_data.get("rmbme"):
            session.permanent = True
        else:
            session.permanent = False
        
        if account["admin"] == 1:
            session["admin"] = True
        else:
            session["admin"] = False

        session["logged_in"] = True
        session["userId"] = account["usersId"]
        session["userUid"] = account["usersUid"]
        session["userEmail"] = account["usersEmail"]
        session["userPwd"] = account["usersPwd"]

        return redirect(url_for(".fiok", message="sikeres-bejelentkezes"))

    else: 
        return redirect(url_for(".bejelentkezes", message="rossz-adatok"))


    # Database connection close
    conn.commit()
    conn.close()
    cursor.close()

@app.route("/register_inc", methods=["POST", "GET"])
def register_inc():

    # Database connection
    conn = pymysql.connect(host="localhost", user="root", passwd="", database="computerdesk")
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Creating variable for data in forms for easy access
    form_data = request.form

    pwdLen = len(form_data["pwd"])
    whitespace = " " in form_data["name"]

    if pwdLen >= 6 and form_data["pwd"] == form_data["pwdrepeat"] and whitespace:

        hashAndSalt = bcrypt.hashpw(form_data["pwd"].encode("utf-8"), bcrypt.gensalt())

        # Insert account data to database
        insert = "INSERT INTO users(usersUid, usersName, usersEmail, usersPwd, regDate) VALUES(%s, %s, %s, %s, %s)"
        cursor.execute(insert, (form_data["uid"], form_data["name"], form_data["email"], hashAndSalt, now.strftime("%d. %B %Y, %H:%M")))

    elif pwdLen <= 6:
        return redirect(url_for(".regisztracio", message="pwd-hossz"))

    elif form_data["pwd"] != form_data["pwdrepeat"]:
        return redirect(url_for(".regisztracio", message="pwd-nem-egyeznek"))
    
    elif not whitespace:
        return redirect(url_for(".regisztracio", message="nem-teljes-név"))

    else:
        return redirect(url_for(".regisztracio", message="ismeretlen-hiba"))

    # Database connection close

    conn.commit()
    conn.close()
    cursor.close()

    return redirect(url_for(".bejelentkezes", message="sikeres-regisztracio"))


@app.route("/fiok")
def fiok():
    if session["admin"] == True:
        conn = pymysql.connect(host="localhost", user="root", passwd="", database="computerdesk")
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT * FROM products WHERE id=(SELECT MAX(id) FROM products)")
        row = cursor.fetchone()
        old_code = row["code"]

        old_code_number = int(re.search(r'\d+', old_code).group())
        old_code = old_code[:-2]

        old_code_number += 1
        old_code += str(old_code_number)

        cursor.execute("SELECT * FROM products")
        products_rows = cursor.fetchall()

        cursor.execute("SELECT * FROM users")
        users_rows = cursor.fetchall()

        return render_template("account.html", site="acc", x=3, users=users_rows, products=products_rows, current=old_code)

    else:
        return render_template("account.html", site="acc", x=3)


@app.route("/bejelentkezes")
def bejelentkezes():
    return render_template("account.html", x=1, site="acc")


@app.route("/regisztracio")
def regisztracio():
    return render_template("account.html", x=2, site="acc")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("userId", None)
    session.pop("userUid", None)
    session.pop("userEmail", None)
    session.pop("userPwd", None)
    session.pop("cartItem", None)
    return redirect(url_for(".bejelentkezes", message="sikeres-kijelentkezes"))  

@app.route("/pwdchange_inc", methods=["POST", "GET"])
def pwdchange():

    # Database connection
    conn = pymysql.connect(host="localhost", user="root", passwd="", database="computerdesk")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT * FROM users WHERE usersUid = %s", (session["userUid"]))
    account = cursor.fetchone()

    form_data = request.form

    valid = bcrypt.checkpw(form_data["oldPwd"].encode("utf-8"), account["usersPwd"].encode("utf-8"))

    pwdLen = len(form_data["newPwd"]) 

    if valid and form_data["newPwd"] == form_data["newPwdRepeat"] and pwdLen >= 6 and form_data["newPwd"] != form_data["oldPwd"]:
       
        cursor.execute("UPDATE usersPwd SET=%s FROM users WHERE usersUid=%s", (form_data["newPwd"], session["userUid"]))

        return redirect(url_for(".fiok", message="sikeres-jelszo-valtoztatas"))

    elif form_data["newPwd"] != form_data["newPwdRepeat"]:
        return redirect(url_for(".fiok", message="pwdk-nem-egyeznek"))

    elif form_data["oldPwd"] != session["userPwd"]:
        return redirect(url_for(".fiok", message="hibas-pwd"))
    
    elif pwdLen < 6:
        return redirect(url_for(".fiok", message="pwd-nem-6"))

    elif form_data["newPwd"] == form_data["oldPwd"]:
        return redirect(url_for(".fiok", message="pwd-egyezik"))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)