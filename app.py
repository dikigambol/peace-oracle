from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template
from modules.zodiak.routes import zodiak_bp
from modules.shio.routes import shio_bp

app = Flask(__name__, template_folder="core/templates", static_folder="core/static")
app.register_blueprint(zodiak_bp)
app.register_blueprint(shio_bp)


@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
