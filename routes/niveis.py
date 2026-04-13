from flask import Blueprint, render_template, request, redirect, url_for, flash

from extensions import db
from models import Nivel, Atleta, Categoria
from utils import admin_required

niveis_bp = Blueprint("niveis", __name__)


@niveis_bp.route("/niveis")
@admin_required
def listar_niveis():
    niveis = Nivel.query.order_by(Nivel.nome.asc()).all()
    return render_template("niveis.html", niveis=niveis)


@niveis_bp.route("/niveis/novo", methods=["GET", "POST"])
@admin_required
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


@niveis_bp.route("/niveis/editar/<int:nivel_id>", methods=["GET", "POST"])
@admin_required
def editar_nivel(nivel_id):
    nivel = Nivel.query.get_or_404(nivel_id)

    if request.method == "POST":
        novo_nome = request.form.get("nome")

        if not novo_nome or not novo_nome.strip():
            flash("Informe um nome válido para o nível.", "error")
            return redirect(url_for("niveis.editar_nivel", nivel_id=nivel.id))

        novo_nome = novo_nome.strip()

        existente = Nivel.query.filter(
            db.func.lower(Nivel.nome) == novo_nome.lower()
        ).first()

        if existente and existente.id != nivel.id:
            flash("Já existe um nível com esse nome.", "error")
            return redirect(url_for("niveis.editar_nivel", nivel_id=nivel.id))

        nivel.nome = novo_nome
        db.session.commit()

        flash("Nível atualizado com sucesso!", "success")
        return redirect(url_for("niveis.listar_niveis"))

    return render_template("editar_nivel.html", nivel=nivel)


@niveis_bp.route("/niveis/excluir/<int:nivel_id>", methods=["POST"])
@admin_required
def excluir_nivel(nivel_id):
    nivel = Nivel.query.get_or_404(nivel_id)

    atleta_vinculado = Atleta.query.filter_by(nivel_id=nivel.id).first()
    categoria_vinculada = Categoria.query.filter_by(nivel_id=nivel.id).first()

    if atleta_vinculado or categoria_vinculada:
        flash(
            "Este nível não pode ser excluído porque está vinculado a atletas ou categorias.",
            "error"
        )
        return redirect(url_for("niveis.listar_niveis"))

    db.session.delete(nivel)
    db.session.commit()

    flash("Nível excluído com sucesso!", "success")
    return redirect(url_for("niveis.listar_niveis"))