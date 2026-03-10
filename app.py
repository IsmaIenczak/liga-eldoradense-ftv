import os
from dotenv import load_dotenv
from flask import Flask, render_template

from extensions import db

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///liga.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def home():
    return render_template("index.html")


from routes.atletas import atletas_bp
from routes.eventos import eventos_bp
from routes.categorias import categorias_bp
from routes.inscricoes import inscricoes_bp

app.register_blueprint(atletas_bp)
app.register_blueprint(eventos_bp)
app.register_blueprint(categorias_bp)
app.register_blueprint(inscricoes_bp)


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)