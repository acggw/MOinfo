from flask import Blueprint, render_template, request, redirect, session, url_for
from database.tables.user import User
from database.tables.bills import Bill
from server.sql_conn import db
from sqlalchemy.orm import joinedload

admin_bp = Blueprint("admin", __name__, template_folder="templates/auth")

@admin_bp.route("/admin/users", methods=["GET"])
def display_users():
    users = db.session.query(User).options(joinedload(User.preferences)).all()
    return render_template("admin/users.html", users=users)

@admin_bp.route("/admin/bills", methods=["GET"])
def display_bills():
    bills = Bill.query.options(joinedload(Bill.actions)).all()
    return render_template("admin/bills.html", bills=bills)