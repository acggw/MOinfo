from flask import Flask, render_template
from auth.routes import auth_bp
#from prefs.routes import prefs_bp

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET_KEY"

# Register Blueprints
app.register_blueprint(auth_bp)
#app.register_blueprint(prefs_bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
