from flask import Flask
from modules.zodiak.routes import zodiak_bp
from modules.shio.routes import shio_bp

app = Flask(__name__, template_folder="core/templates", static_folder="core/static")

# Register blueprints
app.register_blueprint(zodiak_bp)
app.register_blueprint(shio_bp)

if __name__ == "__main__":
    app.run(debug=True)
