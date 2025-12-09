from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from ...Scripts.errors import Errors
from create_user import create_user

auth_bp = Blueprint("auth", __name__, template_folder="templates/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        if verify_user(user, password):
            session["user_id"] = user
            return redirect("/prefs")
        else:
            return "Invalid username or password"
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form["username"]

        password = request.form["password"]

        email = request.form["email"]

        phone = request.form["phone"]

        try:
            create_user(user, password, email, phone)
            return redirect("/login")
        except Errors.DUPLICATE_USER_NAME_ERROR:
            return "Username already exists"
        except Errors.DUPLICATE_EMAIL_ERROR:
            return "Another user registered with that email"
        except Errors.DUPLICATE_PHONE_ERROR:
            return "Another user registered with that phone number"
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/index")
