import os
from dotenv import load_dotenv
from flask import Flask, render_template
from extensions import db
from models import Atleta, Evento, Categoria, Inscricao
from routes.niveis import niveis_bp




load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///liga.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)




@app.route("/")
def home():
    total_atletas = Atleta.query.count()
    total_eventos = Evento.query.count()
    total_categorias = Categoria.query.count()
    total_inscricoes = Inscricao.query.count()

    categorias = Categoria.query.all()
    categorias_lotadas = sum(1 for categoria in categorias if len(categoria.inscricoes) >= categoria.vagas)

    eventos = Evento.query.order_by(Evento.data.asc()).all()

    return render_template(
        "index.html",
        total_atletas=total_atletas,
        total_eventos=total_eventos,
        total_categorias=total_categorias,
        total_inscricoes=total_inscricoes,
        categorias_lotadas=categorias_lotadas,
        eventos=eventos
    )


from routes.atletas import atletas_bp
from routes.eventos import eventos_bp
from routes.categorias import categorias_bp
from routes.inscricoes import inscricoes_bp


app.register_blueprint(atletas_bp)
app.register_blueprint(eventos_bp)
app.register_blueprint(categorias_bp)
app.register_blueprint(inscricoes_bp)
app.register_blueprint(niveis_bp)

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)