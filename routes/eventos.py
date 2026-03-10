from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import Evento

eventos_bp = Blueprint("eventos", __name__)


@eventos_bp.route("/eventos")
def listar_eventos():
    eventos = Evento.query.all()
    return render_template("eventos.html", eventos=eventos)


@eventos_bp.route("/eventos/novo", methods=["GET", "POST"])
def cadastrar_evento():
    if request.method == "POST":
        nome = request.form.get("nome")
        data_str = request.form.get("data")
        arena = request.form.get("arena")
        rua = request.form.get("rua")
        cidade = request.form.get("cidade")
        cep = request.form.get("cep")
        numero = request.form.get("numero")

        data = datetime.strptime(data_str, "%Y-%m-%d").date()

        novo_evento = Evento(
            nome=nome,
            data=data,
            arena=arena,
            rua=rua,
            cidade=cidade,
            cep=cep,
            numero=numero
        )

        db.session.add(novo_evento)
        db.session.commit()

        return redirect(url_for("eventos.listar_eventos"))

    return render_template("novo_evento.html")