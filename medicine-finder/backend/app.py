import os

from flask import Flask, render_template
from sqlalchemy import text

from config import Config
from database import db
from routes.auth import auth_bp
from routes.medicine import medicine_bp
from routes.pharmacy import pharmacy_bp
from routes.user import user_bp


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")


app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND_DIR, "templates"),
    static_folder=os.path.join(FRONTEND_DIR, "static"),
    instance_path=os.path.join(PROJECT_ROOT, "instance"),
    instance_relative_config=True,
)

app.config.from_object(Config)
os.makedirs(app.instance_path, exist_ok=True)

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(pharmacy_bp)
app.register_blueprint(medicine_bp)


@app.route("/")
def index():
    return render_template("index.html")


def ensure_pharmacy_location_columns():
    existing = {
        row[1]
        for row in db.session.execute(text("PRAGMA table_info(pharmacies)")).fetchall()
    }

    column_defs = {
        "street": "ALTER TABLE pharmacies ADD COLUMN street VARCHAR(255)",
        "state": "ALTER TABLE pharmacies ADD COLUMN state VARCHAR(120)",
        "pincode": "ALTER TABLE pharmacies ADD COLUMN pincode VARCHAR(20)",
        "country": "ALTER TABLE pharmacies ADD COLUMN country VARCHAR(120)",
    }

    for col, stmt in column_defs.items():
        if col not in existing:
            db.session.execute(text(stmt))

    db.session.commit()


with app.app_context():
    db.create_all()
    ensure_pharmacy_location_columns()


if __name__ == "__main__":
    app.run(debug=True)