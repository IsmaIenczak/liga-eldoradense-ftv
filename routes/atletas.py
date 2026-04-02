from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import or_
from extensions import db
from models import Atleta, Inscricao
from models import Atleta, Inscricao, Nivel

atletas_bp = Blueprint("atletas", __name__)


@atletas_bp.route("/atletas")
def listar_atletas():
    atletas = Atleta.query.all()
    return render_template("atletas.html", atletas=atletas)


@atletas_bp.route("/atletas/novo", methods=["GET", "POST"])
def cadastrar_atleta():
    niveis = Nivel.query.order_by(Nivel.nome.asc()).all()

    if request.method == "POST":
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        sexo = request.form.get("sexo")
        nivel_id = request.form.get("nivel")

        if not cpf.isdigit() or len(cpf) != 11:
            return render_template(
                "novo_atleta.html",
                erro="CPF deve conter exatamente 11 números.",
                niveis=niveis
            )

        cpf_existente = Atleta.query.filter_by(cpf=cpf).first()
        if cpf_existente:
            return render_template(
                "novo_atleta.html",
                erro="CPF já cadastrado no sistema.",
                niveis=niveis
            )

        novo_atleta = Atleta(
            nome=nome,
            cpf=cpf,
            sexo=sexo,
            nivel_id=int(nivel_id)
        )

        db.session.add(novo_atleta)
        db.session.commit()

        return redirect(url_for("atletas.listar_atletas"))

    return render_template("novo_atleta.html", niveis=niveis)




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
    niveis = Nivel.query.order_by(Nivel.nome.asc()).all()

    if request.method == "POST":
        novo_nome = request.form.get("nome")
        novo_cpf = request.form.get("cpf")
        novo_sexo = request.form.get("sexo")
        novo_nivel_id = int(request.form.get("nivel"))

        if not novo_cpf.isdigit() or len(novo_cpf) != 11:
            flash("CPF deve conter exatamente 11 números.", "error")
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
            modalidade = categoria.modalidade.strip().lower()

            if novo_nivel_id != parceiro.nivel_id:
                flash(
                    f"Não é possível alterar este atleta: a inscrição com {parceiro.nome} ficaria com níveis diferentes.",
                    "error"
                )
                return redirect(url_for("atletas.editar_atleta", atleta_id=atleta_id))

            if novo_nivel_id != categoria.nivel_id:
                flash(
                    f"Não é possível alterar este atleta: a inscrição na categoria {categoria.nome} ficaria com nível incompatível.",
                    "error"
                )
                return redirect(url_for("atletas.editar_atleta", atleta_id=atleta_id))

            novo_sexo_normalizado = novo_sexo.strip().lower()

            if modalidade == "masculino":
                if novo_sexo_normalizado != "masculino" or parceiro_sexo != "masculino":
                    flash(
                        f"Não é possível alterar este atleta: a inscrição na categoria {categoria.nome} exige dupla masculina.",
                        "error"
                    )
                    return redirect(url_for("atletas.editar_atleta", atleta_id=atleta_id))

            elif modalidade == "feminino":
                if novo_sexo_normalizado != "feminino" or parceiro_sexo != "feminino":
                    flash(
                        f"Não é possível alterar este atleta: a inscrição na categoria {categoria.nome} exige dupla feminina.",
                        "error"
                    )
                    return redirect(url_for("atletas.editar_atleta", atleta_id=atleta_id))

            elif modalidade == "misto":
                if novo_sexo_normalizado == parceiro_sexo:
                    flash(
                        f"Não é possível alterar este atleta: a inscrição na categoria {categoria.nome} deixaria de ser mista.",
                        "error"
                    )
                    return redirect(url_for("atletas.editar_atleta", atleta_id=atleta_id))

        atleta.nome = novo_nome
        atleta.cpf = novo_cpf
        atleta.sexo = novo_sexo
        atleta.nivel_id = novo_nivel_id

        db.session.commit()

        flash("Atleta atualizado com sucesso!", "success")
        return redirect(url_for("atletas.listar_atletas"))

    return render_template("editar_atleta.html", atleta=atleta, niveis=niveis)