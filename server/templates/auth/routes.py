from flask import Blueprint, render_template, request, redirect, session, url_for
from config.errors import Errors
from database.tables.user import verify_user, create_user
from server.sql_conn import db

auth_bp = Blueprint("auth", __name__, template_folder="templates/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        if verify_user(db.session, user, password):
            session["username"] = user
            return return_from()
        else:
            return "Invalid username or password"
    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form["username"]

        password = request.form["password"]

        email = request.form["email"]

        phone = request.form["phone"]

        try:
            create_user(db.session, user, password, email, phone)
            session["username"] = user
            return return_from()
        except Errors.DUPLICATE_USER_NAME_ERROR:
            return "Username already exists"
        except Errors.DUPLICATE_EMAIL_ERROR:
            return "Another user registered with that email"
        except Errors.DUPLICATE_PHONE_ERROR:
            return "Another user registered with that phone number"
    return render_template("auth/register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return return_from()

def return_from():
    if "last_on" in session:
        return redirect(session["last_on"])
    return redirect(url_for("index"))
