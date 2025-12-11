from flask import Flask, render_template

from server.templates.auth.routes import auth_bp
from server.templates.pref.routes import pref_bp
from server.templates.admin.routes import admin_bp
from server.templates.bills.routes import bill_bp

from config.database import DATABASE_URL
from server.sql_conn import db

import os

def create_app():
    app = Flask(__name__)
    app.secret_key = "CHANGE_THIS_SECRET_KEY"

    # ---- Add your database configuration here ----

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize Flask-SQLAlchemy with the app
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(pref_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(bill_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


# Run the app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
