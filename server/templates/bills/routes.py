from flask import Blueprint, render_template
from server.sql_conn import db
from database.tables.bills import retreive_bill, Bill

bill_bp = Blueprint("bills", __name__, template_folder="templates/pref")

@bill_bp.route("/bills/<chamber>/<session>/<bill_id>", methods=["GET"])
def bill_page(chamber, session, bill_id):
    bill = retreive_bill(db.session, chamber, session, bill_id)
    return render_template("bills/bills.html", bill=bill)

@bill_bp.route("/bills")
def all_bills():
    bills = db.session.select(Bill).all()
    return render_template("bills/index.html", bills=bills)