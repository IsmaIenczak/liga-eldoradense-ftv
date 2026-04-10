import os
from dotenv import load_dotenv
from flask import Flask, render_template, session, redirect, url_for, request
from extensions import db
from models import Atleta, Evento, Categoria, Inscricao, Usuario
from routes.niveis import niveis_bp
from datetime import timedelta




load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///liga.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.permanent_session_lifetime = timedelta(minutes=30)

@app.before_request
def proteger_rotas():
    rotas_livres = ["auth.login", "static"]

    if request.endpoint is None:
        return

    if request.endpoint in rotas_livres:
        return

    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))



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
from routes.auth import auth_bp


app.register_blueprint(atletas_bp)
app.register_blueprint(eventos_bp)
app.register_blueprint(categorias_bp)
app.register_blueprint(inscricoes_bp)
app.register_blueprint(niveis_bp)
app.register_blueprint(auth_bp)



with app.app_context():
    db.create_all()

    admin_existente = Usuario.query.filter_by(email="admin@admin.com").first()

    if not admin_existente:
        admin = Usuario(
            email="admin@admin.com",
            tipo="admin"
        )
        admin.set_senha("Admin@Liga2026!")

        db.session.add(admin)
        db.session.commit()

        print("Admin criado com sucesso: admin@admin.com")




if __name__ == "__main__":
    app.run(debug=True)