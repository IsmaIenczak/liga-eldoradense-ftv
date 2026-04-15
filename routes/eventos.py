from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash

from extensions import db
from models import Evento
from utils import admin_required

eventos_bp = Blueprint("eventos", __name__)


@eventos_bp.route("/eventos")
@admin_required
def listar_eventos():
    eventos = Evento.query.all()
    return render_template("eventos.html", eventos=eventos)


@eventos_bp.route("/eventos/novo", methods=["GET", "POST"])
@admin_required
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

        if data < date.today():
            flash("A data do evento não pode estar no passado.", "error")
            return redirect(url_for("eventos.cadastrar_evento"))

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

        flash("Evento criado com sucesso!", "success")
        return redirect(url_for("eventos.listar_eventos"))

    return render_template("novo_evento.html")




@eventos_bp.route("/eventos/editar/<int:evento_id>", methods=["GET", "POST"])
@admin_required
def editar_evento(evento_id):
    evento = Evento.query.get_or_404(evento_id)

    if request.method == "POST":
        nome = request.form.get("nome")
        data_str = request.form.get("data")
        arena = request.form.get("arena")
        rua = request.form.get("rua")
        cidade = request.form.get("cidade")
        cep = request.form.get("cep")
        numero = request.form.get("numero")

        data = datetime.strptime(data_str, "%Y-%m-%d").date()

        if data < date.today():
            flash("A data do evento não pode estar no passado.", "error")
            return redirect(url_for("eventos.editar_evento", evento_id=evento_id))

        evento.nome = nome
        evento.data = data
        evento.arena = arena
        evento.rua = rua
        evento.cidade = cidade
        evento.cep = cep
        evento.numero = numero

        db.session.commit()

        flash("Evento atualizado com sucesso!", "success")
        return redirect(url_for("eventos.listar_eventos"))

    return render_template("editar_evento.html", evento=evento)




@eventos_bp.route("/eventos/excluir/<int:evento_id>", methods=["POST"])
@admin_required
def excluir_evento(evento_id):
    evento = Evento.query.get_or_404(evento_id)

    if evento.categorias:
        flash(
            "Este evento não pode ser excluído porque possui categorias vinculadas.",
            "error"
        )
        return redirect(url_for("eventos.listar_eventos"))

    db.session.delete(evento)
    db.session.commit()

    flash("Evento excluído com sucesso!", "success")
    return redirect(url_for("eventos.listar_eventos"))