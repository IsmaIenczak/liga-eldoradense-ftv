from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Nivel

niveis_bp = Blueprint("niveis", __name__)


@niveis_bp.route("/niveis")
def listar_niveis():
    niveis = Nivel.query.order_by(Nivel.nome.asc()).all()
    return render_template("niveis.html", niveis=niveis)


@niveis_bp.route("/niveis/novo", methods=["GET", "POST"])
def novo_nivel():
    if request.method == "POST":
        nome = request.form.get("nome")

        if not nome or not nome.strip():
            flash("Informe um nome válido para o nível.", "error")
            return redirect(url_for("niveis.novo_nivel"))

        nome = nome.strip()

        existente = Nivel.query.filter(db.func.lower(Nivel.nome) == nome.lower()).first()
        if existente:
            flash("Esse nível já está cadastrado.", "error")
            return redirect(url_for("niveis.novo_nivel"))

        nivel = Nivel(nome=nome)
        db.session.add(nivel)
        db.session.commit()

        flash("Nível cadastrado com sucesso!", "success")
        return redirect(url_for("niveis.listar_niveis"))

    return render_template("novo_nivel.html")