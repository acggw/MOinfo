from flask import Blueprint, render_template, request, redirect, url_for, session
from database.tables.user import set_preference
from server.sql_conn import db

pref_bp = Blueprint("pref", __name__, template_folder="templates/pref")

categories = [
    "Technology", "Science", "Health", "Finance", "Sports", 
    "Education", "Entertainment", "Politics", "Travel", "Food"
    # This list can be much longer
]

@pref_bp.route("/pref", methods=["GET", "POST"])
def preferences():
    if "username" not in session:
        session["last_on"] = url_for("pref.preferences")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        # Grab selected categories and interest levels
        selected_categories = request.form.getlist("category")
        interests = {cat: request.form.get(f"interest_{cat}") for cat in selected_categories}
        for interest, level in interests.items():
            set_preference(db.session, session["username"], interest, level)

        return redirect(url_for("pref.preferences"))

    return render_template("pref/pref.html", categories=categories)