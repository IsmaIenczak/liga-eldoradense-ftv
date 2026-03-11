from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import or_

from extensions import db
from models import Atleta, Inscricao

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




@atletas_bp.route("/atletas/excluir/<int:atleta_id>", methods=["POST"])
def excluir_atleta(atleta_id):
    atleta = Atleta.query.get_or_404(atleta_id)

    inscricao_existente = Inscricao.query.filter(
        or_(
            Inscricao.atleta1_id == atleta_id,
            Inscricao.atleta2_id == atleta_id
        )
    ).first()

    if inscricao_existente:
        flash("Este atleta não pode ser excluído porque já está vinculado a uma inscrição.", "error")
        return redirect(url_for("atletas.listar_atletas"))

    db.session.delete(atleta)
    db.session.commit()

    flash("Atleta excluído com sucesso!", "success")
    return redirect(url_for("atletas.listar_atletas"))



@atletas_bp.route("/atletas/editar/<int:atleta_id>", methods=["GET", "POST"])
def editar_atleta(atleta_id):
    atleta = Atleta.query.get_or_404(atleta_id)

    if request.method == "POST":
        novo_nome = request.form.get("nome")
        novo_cpf = request.form.get("cpf")
        novo_sexo = request.form.get("sexo")
        novo_nivel = request.form.get("nivel")

        if not novo_cpf.isdigit() or len(novo_cpf) != 11:
            flash("CPF deve conter exatamente 11 números (somente números).", "error")
            return redirect(url_for("atletas.editar_atleta", atleta_id=atleta_id))

        cpf_existente = Atleta.query.filter_by(cpf=novo_cpf).first()
        if cpf_existente and cpf_existente.id != atleta.id:
            flash("CPF já cadastrado para outro atleta.", "error")
            return redirect(url_for("atletas.editar_atleta", atleta_id=atleta_id))

        inscricoes = Inscricao.query.filter(
            or_(
                Inscricao.atleta1_id == atleta.id,
                Inscricao.atleta2_id == atleta.id
            )
        ).all()

        for inscricao in inscricoes:
            categoria = inscricao.categoria
            parceiro = inscricao.atleta2 if inscricao.atleta1_id == atleta.id else inscricao.atleta1

            parceiro_sexo = parceiro.sexo.strip().lower()
            parceiro_nivel = parceiro.nivel.strip().lower()
            modalidade = categoria.modalidade.strip().lower()
            categoria_nivel = categoria.nivel.strip().lower()

            novo_sexo_normalizado = novo_sexo.strip().lower()
            novo_nivel_normalizado = novo_nivel.strip().lower()

            # Regra: atleta e parceiro precisam continuar no mesmo nível
            if novo_nivel_normalizado != parceiro_nivel:
                flash(
                    f"Não é possível alterar este atleta: a inscrição com {parceiro.nome} ficaria com níveis diferentes. Cancele/exclua a inscrição antes de realizar essa alteração.",
                    "error"
                )
                return redirect(url_for("atletas.editar_atleta", atleta_id=atleta_id))

            # Regra: nível do atleta precisa continuar compatível com a categoria
            if novo_nivel_normalizado != categoria_nivel:
                flash(
                    f"Não é possível alterar este atleta: a inscrição na categoria {categoria.nome} ficaria com nível incompatível. Cancele/exclua a inscrição antes de realizar essa alteração.",
                    "error"
                )
                return redirect(url_for("atletas.editar_atleta", atleta_id=atleta_id))

            # Regra: sexo precisa continuar compatível com a modalidade
            if modalidade == "masculino":
                if novo_sexo_normalizado != "masculino" or parceiro_sexo != "masculino":
                    flash(
                        f"Não é possível alterar este atleta: a inscrição na categoria {categoria.nome} exige dupla masculina. Cancele/exclua a inscrição antes de realizar essa alteração.",
                        "error"
                    )
                    return redirect(url_for("atletas.editar_atleta", atleta_id=atleta_id))

            elif modalidade == "feminino":
                if novo_sexo_normalizado != "feminino" or parceiro_sexo != "feminino":
                    flash(
                        f"Não é possível alterar este atleta: a inscrição na categoria {categoria.nome} exige dupla feminina. Cancele/exclua a inscrição antes de realizar essa alteração.",
                        "error"
                    )
                    return redirect(url_for("atletas.editar_atleta", atleta_id=atleta_id))

            elif modalidade == "misto":
                if novo_sexo_normalizado == parceiro_sexo:
                    flash(
                        f"Não é possível alterar este atleta: a inscrição na categoria {categoria.nome} deixaria de ser mista. Cancele/exclua a inscrição antes de realizar essa alteração.",
                        "error"
                    )
                    return redirect(url_for("atletas.editar_atleta", atleta_id=atleta_id))

        atleta.nome = novo_nome
        atleta.cpf = novo_cpf
        atleta.sexo = novo_sexo
        atleta.nivel = novo_nivel

        db.session.commit()

        flash("Atleta atualizado com sucesso!", "success")
        return redirect(url_for("atletas.listar_atletas"))

    return render_template("editar_atleta.html", atleta=atleta)