from flask import Flask
from flask import render_template
from flask import session
from flask import request
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = 'oh_so_secret'

# User credentials data

stored_credentials = {"tristar": "password"}

# Check if user is authenticated

def check_user_login_state():
    if session.get("logged_in"):
        print("User is already authenticated, returning True")
        return True
    else:
        print("User is not authenticated, returning False")

def pwd_logic(username, password):

        for i in stored_credentials:
            if stored_credentials[username] == password:
                print("Authenticated")
                session["logged_in"] = True
                return True
            else:
                print("Wrong username or password")
                return False


def update_news():
    db = sqlite3.connect("./news.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM news_text ORDER BY ID DESC LIMIT 5")
    news_data = cursor.fetchall()
    print(news_data)
    db.close()


@app.route('/')
@app.route('/index.html', methods=["GET", "POST"])
def index():

    if check_user_login_state():
        return render_template("index.html")
    else:
        return render_template("login.html")

@app.route("/login.html", methods=["GET","POST"])
def login():

    if check_user_login_state():
        return render_template("already_logged_in.html")

    else:
        if request.method == "POST":
            print(request.form.get("auth_form"))
            if request.form.get("auth_form") == "submit":
                username = request.form["form_username"]
                password = request.form["form_password"]
                pwd_logic(username, password)

                if pwd_logic(username, password):
                    return render_template("index.html")

        return render_template("login.html")

@app.route("/already_logged_in.html", methods=["GET","POST"])
def already_logged_in():

    if request.method == "POST":
        print(request.form)
        if request.form.get("logout") == "submit":
            print("processing...")
            session["logged_in"] = False

        return render_template("login.html")


    return render_template("already_logged_in.html")

@app.route("/news.html", methods=["GET","POST"])
def news():

    # Print out news
    update_news()



    #Form handler...

    if request.method == "POST":
        if request.form.get("news_form") == "submit":

            try:
                news_text = request.form["news_body"]
                db = sqlite3.connect("./news.db")
                cursor = db.cursor()
                cursor.execute("INSERT INTO news_text (news_text) VALUES (?)", (news_text,))
                db.commit()

            except Exception as ex:
                print(ex)

        update_news()

    return render_template("news.html", news_data=news_data)


if __name__ == '__main__':
    app.run()
