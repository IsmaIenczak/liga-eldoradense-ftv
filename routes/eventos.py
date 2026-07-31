from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash

from extensions import db
from models import Evento
from utils import admin_required, normalizar_cep


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
        numero_raw = request.form.get("numero")

        if not nome or not nome.strip():
            flash("Informe um nome válido para o evento.", "error")
            return redirect(url_for("eventos.cadastrar_evento"))

        if not data_str:
            flash("Informe uma data válida para o evento.", "error")
            return redirect(url_for("eventos.cadastrar_evento"))

        try:
            data = datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            flash("A data do evento deve estar no formato YYYY-MM-DD.", "error")
            return redirect(url_for("eventos.cadastrar_evento"))

        if data < date.today():
            flash("A data do evento não pode estar no passado.", "error")
            return redirect(url_for("eventos.cadastrar_evento"))

        if not arena or not arena.strip():
            flash("Informe a arena do evento.", "error")
            return redirect(url_for("eventos.cadastrar_evento"))

        if not rua or not rua.strip():
            flash("Informe a rua do evento.", "error")
            return redirect(url_for("eventos.cadastrar_evento"))

        if not cidade or not cidade.strip():
            flash("Informe a cidade do evento.", "error")
            return redirect(url_for("eventos.cadastrar_evento"))

        cep = normalizar_cep(cep)
        if cep is None:
            flash("Informe um CEP válido com 8 dígitos.", "error")
            return redirect(url_for("eventos.cadastrar_evento"))

        try:
            numero = int(numero_raw)
        except (TypeError, ValueError):
            flash("Informe um número de endereço válido.", "error")
            return redirect(url_for("eventos.cadastrar_evento"))

        novo_evento = Evento(
            nome=nome.strip(),
            data=data,
            arena=arena.strip(),
            rua=rua.strip(),
            cidade=cidade.strip(),
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
        numero_raw = request.form.get("numero")

        if not nome or not nome.strip():
            flash("Informe um nome válido para o evento.", "error")
            return redirect(url_for("eventos.editar_evento", evento_id=evento_id))

        if not data_str:
            flash("Informe uma data válida para o evento.", "error")
            return redirect(url_for("eventos.editar_evento", evento_id=evento_id))

        try:
            data = datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            flash("A data do evento deve estar no formato YYYY-MM-DD.", "error")
            return redirect(url_for("eventos.editar_evento", evento_id=evento_id))

        if data < date.today():
            flash("A data do evento não pode estar no passado.", "error")
            return redirect(url_for("eventos.editar_evento", evento_id=evento_id))

        if not arena or not arena.strip():
            flash("Informe a arena do evento.", "error")
            return redirect(url_for("eventos.editar_evento", evento_id=evento_id))

        if not rua or not rua.strip():
            flash("Informe a rua do evento.", "error")
            return redirect(url_for("eventos.editar_evento", evento_id=evento_id))

        if not cidade or not cidade.strip():
            flash("Informe a cidade do evento.", "error")
            return redirect(url_for("eventos.editar_evento", evento_id=evento_id))

        cep = normalizar_cep(cep)
        if cep is None:
            flash("Informe um CEP válido com 8 dígitos.", "error")
            return redirect(url_for("eventos.editar_evento", evento_id=evento_id))

        try:
            numero = int(numero_raw)
        except (TypeError, ValueError):
            flash("Informe um número de endereço válido.", "error")
            return redirect(url_for("eventos.editar_evento", evento_id=evento_id))

        evento.nome = nome.strip()
        evento.data = data
        evento.arena = arena.strip()
        evento.rua = rua.strip()
        evento.cidade = cidade.strip()
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
