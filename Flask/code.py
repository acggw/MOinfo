from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from Scripts.user_prefs.register import register_user
from Scripts.errors import Errors

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET_KEY"

# --------------------------
# Routes
# --------------------------

@app.route("/")
def index():
    '''
    if "user_id" in session:
        return redirect("/prefs")
    return redirect("/login")
    '''
    return render_template("index.html")


# ---------- Register ----------
@app.route("/auth/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form["username"]

        password = request.form["password"]
        pw_hash = generate_password_hash(password)

        email = request.form["email"]

        phone = request.form["phone"]

        try:
            register_user(user, pw_hash, email, phone)
            return redirect("/login")
        except Errors.DUPLICATE_USER_NAME_ERROR:
            return "Username already exists"
        except Errors.DUPLICATE_EMAIL_ERROR:
            return "Another user registered with that email"
        except Errors.DUPLICATE_PHONE_ERROR:
            return "Another user registered with that phone number"

    return render_template("register.html")


# ---------- Login ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.execute("SELECT id, password_hash FROM users WHERE username = ?", (user,))
        row = cur.fetchone()
        conn.close()

        if row and check_password_hash(row[1], password):
            session["user_id"] = row[0]
            return redirect("/prefs")
        else:
            return "Invalid username or password"

    return render_template("login.html")


# ---------- Logout ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------- Preferences ----------
@app.route("/prefs", methods=["GET", "POST"])
def prefs():
    if "user_id" not in session:
        return redirect("/login")

    uid = session["user_id"]

    conn = get_db()

    if request.method == "POST":
        p1 = request.form["pref1"]
        p2 = request.form["pref2"]

        conn.execute(
            "UPDATE users SET preference1 = ?, preference2 = ? WHERE id = ?",
            (p1, p2, uid)
        )
        conn.commit()

    cur = conn.execute(
        "SELECT preference1, preference2 FROM users WHERE id = ?",
        (uid,)
    )
    prefs = cur.fetchone()
    conn.close()

    p1, p2 = prefs if prefs else ("", "")

    return render_template("prefs.html", pref1=p1, pref2=p2)


if __name__ == "__main__":
    app.run(debug=True)
