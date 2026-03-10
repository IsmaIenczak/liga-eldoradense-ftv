from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import Atleta

atletas_bp = Blueprint("atletas", __name__)


@atletas_bp.route("/atletas")
def listar_atletas():
    atletas = Atleta.query.all()
    return render_template("atletas.html", atletas=atletas)


@atletas_bp.route("/atletas/novo", methods=["GET", "POST"])
def cadastrar_atleta():
    if request.method == "POST":
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        sexo = request.form.get("sexo")
        nivel = request.form.get("nivel")

        if not cpf.isdigit() or len(cpf) != 11:
            return render_template(
                "novo_atleta.html",
                erro="CPF deve conter exatamente 11 números."
            )

        cpf_existente = Atleta.query.filter_by(cpf=cpf).first()
        if cpf_existente:
            return render_template(
                "novo_atleta.html",
                erro="CPF já cadastrado no sistema."
            )

        novo_atleta = Atleta(
            nome=nome,
            cpf=cpf,
            sexo=sexo,
            nivel=nivel
        )

        db.session.add(novo_atleta)
        db.session.commit()

        return redirect(url_for("atletas.listar_atletas"))

    return render_template("novo_atleta.html")