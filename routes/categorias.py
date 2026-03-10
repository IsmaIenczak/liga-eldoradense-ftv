from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Evento, Categoria

categorias_bp = Blueprint("categorias", __name__)


@categorias_bp.route("/categorias/nova", methods=["GET", "POST"])
def nova_categoria():
    eventos = Evento.query.all()

    if request.method == "POST":
        modalidade = request.form.get("modalidade")
        nivel = request.form.get("nivel")
        evento_id = request.form.get("evento")

        existente = Categoria.query.filter_by(
            evento_id=int(evento_id),
            modalidade=modalidade,
            nivel=nivel
        ).first()

        if existente:
            flash("Essa categoria já existe neste evento.", "error")
            return redirect(url_for("categorias.nova_categoria"))

        nova = Categoria(
            modalidade=modalidade,
            nivel=nivel,
            evento_id=int(evento_id)
        )

        db.session.add(nova)
        db.session.commit()

        flash("Categoria criada com sucesso!", "success")
        return redirect(url_for("eventos.listar_eventos"))

    return render_template("nova_categoria.html", eventos=eventos)