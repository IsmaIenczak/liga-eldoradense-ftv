from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from sqlalchemy import or_

from extensions import db
from models import Atleta, Evento, Categoria, Inscricao
from utils import admin_required


inscricoes_bp = Blueprint("inscricoes", __name__)


@inscricoes_bp.route("/api/eventos/<int:evento_id>/categorias")
@admin_required
def api_categorias_por_evento(evento_id):
    categorias = Categoria.query.filter_by(evento_id=evento_id).all()

    return jsonify([
        {
            "id": c.id,
            "nome": c.nome,
            "nivel": c.nivel.nome,
            "modalidade": c.modalidade,
            "vagas": c.vagas,
            "inscritos": len(c.inscricoes),
            "vagas_restantes": c.vagas - len(c.inscricoes),
            "lotada": len(c.inscricoes) >= c.vagas
        }
        for c in categorias
    ])


@inscricoes_bp.route("/inscricoes/nova", methods=["GET", "POST"])
@admin_required
def nova_inscricao():
    atletas = Atleta.query.all()
    eventos = Evento.query.all()

    if not eventos:
        flash("Cadastre um evento antes de criar inscrições.", "error")
        return render_template(
            "nova_inscricao.html",
            atletas=atletas,
            eventos=[],
            categorias=[],
            selected_evento_id=None
        )

    selected_evento_id = request.args.get("evento")
    if selected_evento_id is None:
        selected_evento_id = str(eventos[0].id)

    categorias = Categoria.query.filter_by(evento_id=int(selected_evento_id)).all()

    if request.method == "POST":
        evento_id = request.form.get("evento")
        atleta1_id = request.form.get("atleta1")
        atleta2_id = request.form.get("atleta2")
        categoria_id = request.form.get("categoria")

        atleta1 = Atleta.query.get(atleta1_id)
        atleta2 = Atleta.query.get(atleta2_id)
        categoria = Categoria.query.get(categoria_id)

        if not atleta1 or not atleta2 or not categoria or not evento_id:
            flash("Dados inválidos.", "error")
            return redirect(url_for("inscricoes.nova_inscricao"))

        if not atleta1.residente_eldorado and not atleta2.residente_eldorado:
            flash("Pelo menos um dos atletas da dupla deve ser residente de Eldorado do Sul.", "error")
            return redirect(url_for("inscricoes.nova_inscricao", evento=evento_id))

        if categoria.evento_id != int(evento_id):
            flash("A categoria selecionada não pertence ao evento escolhido.", "error")
            return redirect(url_for("inscricoes.nova_inscricao", evento=evento_id))

        if atleta1_id == atleta2_id:
            flash("Selecione atletas diferentes", "error")
            return redirect(url_for("inscricoes.nova_inscricao", evento=evento_id))

        if atleta1.nivel_id != atleta2.nivel_id:
            flash("Os atletas devem estar no mesmo nível", "error")
            return redirect(url_for("inscricoes.nova_inscricao", evento=evento_id))

        if categoria.nivel_id != atleta1.nivel_id:
            flash("A categoria selecionada deve estar de acordo com nível do atleta", "error")
            return redirect(url_for("inscricoes.nova_inscricao", evento=evento_id))

        modalidade = (categoria.modalidade or "").strip().lower()
        sexo1 = atleta1.sexo.strip().lower()
        sexo2 = atleta2.sexo.strip().lower()

        if modalidade == "masculino":
            if sexo1 != "masculino" or sexo2 != "masculino":
                flash("Essa categoria aceita apenas atletas do sexo masculino.", "error")
                return redirect(url_for("inscricoes.nova_inscricao", evento=evento_id))

        elif modalidade == "feminino":
            if sexo1 != "feminino" or sexo2 != "feminino":
                flash("Essa categoria aceita apenas atletas do sexo feminino.", "error")
                return redirect(url_for("inscricoes.nova_inscricao", evento=evento_id))

        elif modalidade == "misto":
            if sexo1 == sexo2:
                flash("Categoria mista requer um atleta do sexo masculino e um atleta do sexo feminino.", "error")
                return redirect(url_for("inscricoes.nova_inscricao", evento=evento_id))

        inscricoes_categoria = Inscricao.query.filter_by(categoria_id=categoria_id).all()

        if len(inscricoes_categoria) >= categoria.vagas:
            flash(
                f"Esta categoria já atingiu o limite máximo de {categoria.vagas} duplas.",
                "error"
            )
            return redirect(url_for("inscricoes.nova_inscricao", evento=evento_id))

        for inscricao in inscricoes_categoria:
            atletas_existentes = {inscricao.atleta1_id, inscricao.atleta2_id}
            novos_atletas = {int(atleta1_id), int(atleta2_id)}
            if atletas_existentes == novos_atletas:
                flash("Essa dupla já está inscrita nesta categoria.", "error")
                return redirect(url_for("inscricoes.nova_inscricao", evento=evento_id))

        for inscricao in inscricoes_categoria:
            if (
                int(atleta1_id) in [inscricao.atleta1_id, inscricao.atleta2_id] or
                int(atleta2_id) in [inscricao.atleta1_id, inscricao.atleta2_id]
            ):
                flash("Um dos atletas já está inscrito para competir nesta categoria.", "error")
                return redirect(url_for("inscricoes.nova_inscricao", evento=evento_id))

        atletas_pendentes = []

        if not atleta1.nivel_validado:
            atletas_pendentes.append(atleta1.nome)

        if not atleta2.nivel_validado:
            atletas_pendentes.append(atleta2.nome)

        nova = Inscricao(
            atleta1_id=atleta1_id,
            atleta2_id=atleta2_id,
            categoria_id=categoria_id,
            status="confirmada"
        )

        db.session.add(nova)
        db.session.commit()

        flash("Inscrição realizada com sucesso!", "success")

        if atletas_pendentes:
            nomes = ", ".join(atletas_pendentes)
            flash(
                f"Atenção: a inscrição foi realizada, mas o nível do(s) atleta(s) {nomes} ainda não foi validado.",
                "error"
            )

        return redirect(url_for("inscricoes.nova_inscricao", evento=evento_id))

    return render_template(
        "nova_inscricao.html",
        atletas=atletas,
        eventos=eventos,
        categorias=categorias,
        selected_evento_id=int(selected_evento_id)
    )


@inscricoes_bp.route("/inscricoes")
@admin_required
def listar_inscricoes():
    inscricoes = Inscricao.query.all()
    return render_template("inscricoes.html", inscricoes=inscricoes)


@inscricoes_bp.route("/inscricoes/excluir/<int:inscricao_id>", methods=["POST"])
@admin_required
def excluir_inscricao(inscricao_id):
    inscricao = Inscricao.query.get_or_404(inscricao_id)

    db.session.delete(inscricao)
    db.session.commit()

    flash("Inscrição excluída com sucesso!", "success")
    return redirect(url_for("inscricoes.listar_inscricoes"))





@inscricoes_bp.route("/minhas-inscricoes")
def minhas_inscricoes():
    if session.get("usuario_tipo") != "atleta":
        flash("Acesso permitido apenas para atletas.", "error")
        return redirect(url_for("home"))

    atleta_id = session.get("atleta_id")

    inscricoes = Inscricao.query.filter(
        or_(
            Inscricao.atleta1_id == atleta_id,
            Inscricao.atleta2_id == atleta_id
        )
    ).all()

    atleta = Atleta.query.get(atleta_id)

    return render_template(
        "minhas_inscricoes.html",
        inscricoes=inscricoes,
        atleta=atleta
    )






@inscricoes_bp.route("/minha-inscricao/nova", methods=["GET", "POST"])
def nova_inscricao_atleta():
    if session.get("usuario_tipo") != "atleta":
        flash("Acesso permitido apenas para atletas.", "error")
        return redirect(url_for("home"))

    atleta_logado_id = session.get("atleta_id")
    atleta_logado = Atleta.query.get_or_404(atleta_logado_id)

    eventos = Evento.query.all()

    if not eventos:
        flash("Não há eventos disponíveis no momento.", "error")
        return render_template(
            "nova_inscricao_atleta.html",
            atleta_logado=atleta_logado,
            atletas=[],
            eventos=[],
            categorias=[],
            selected_evento_id=None
        )

    selected_evento_id = request.args.get("evento")
    if selected_evento_id is None:
        selected_evento_id = str(eventos[0].id)

    categorias = Categoria.query.filter_by(evento_id=int(selected_evento_id)).all()

    atletas = Atleta.query.filter(Atleta.id != atleta_logado_id).all()

    if request.method == "POST":
        evento_id = request.form.get("evento")
        parceiro_id = request.form.get("parceiro")
        categoria_id = request.form.get("categoria")

        parceiro = Atleta.query.get(parceiro_id)
        categoria = Categoria.query.get(categoria_id)

        if not parceiro or not categoria or not evento_id:
            flash("Dados inválidos.", "error")
            return redirect(url_for("inscricoes.nova_inscricao_atleta"))

        if categoria.evento_id != int(evento_id):
            flash("A categoria selecionada não pertence ao evento escolhido.", "error")
            return redirect(url_for("inscricoes.nova_inscricao_atleta", evento=evento_id))

        if atleta_logado.id == parceiro.id:
            flash("Você não pode formar dupla com você mesmo.", "error")
            return redirect(url_for("inscricoes.nova_inscricao_atleta", evento=evento_id))

        if atleta_logado.nivel_id != parceiro.nivel_id:
            flash("Os atletas devem estar no mesmo nível.", "error")
            return redirect(url_for("inscricoes.nova_inscricao_atleta", evento=evento_id))

        if categoria.nivel_id != atleta_logado.nivel_id:
            flash("A categoria selecionada deve estar de acordo com o nível da dupla.", "error")
            return redirect(url_for("inscricoes.nova_inscricao_atleta", evento=evento_id))

        if not atleta_logado.residente_eldorado and not parceiro.residente_eldorado:
            flash("Pelo menos um dos atletas da dupla deve ser residente de Eldorado do Sul.", "error")
            return redirect(url_for("inscricoes.nova_inscricao_atleta", evento=evento_id))

        modalidade = (categoria.modalidade or "").strip().lower()
        sexo1 = atleta_logado.sexo.strip().lower()
        sexo2 = parceiro.sexo.strip().lower()

        if modalidade == "masculino":
            if sexo1 != "masculino" or sexo2 != "masculino":
                flash("Essa categoria aceita apenas atletas do sexo masculino.", "error")
                return redirect(url_for("inscricoes.nova_inscricao_atleta", evento=evento_id))

        elif modalidade == "feminino":
            if sexo1 != "feminino" or sexo2 != "feminino":
                flash("Essa categoria aceita apenas atletas do sexo feminino.", "error")
                return redirect(url_for("inscricoes.nova_inscricao_atleta", evento=evento_id))

        elif modalidade == "misto":
            if sexo1 == sexo2:
                flash("Categoria mista requer um atleta do sexo masculino e um atleta do sexo feminino.", "error")
                return redirect(url_for("inscricoes.nova_inscricao_atleta", evento=evento_id))

        inscricoes_categoria = Inscricao.query.filter_by(categoria_id=categoria_id).all()

        if len(inscricoes_categoria) >= categoria.vagas:
            flash(
                f"Esta categoria já atingiu o limite máximo de {categoria.vagas} duplas.",
                "error"
            )
            return redirect(url_for("inscricoes.nova_inscricao_atleta", evento=evento_id))

        novos_atletas = {atleta_logado.id, parceiro.id}

        for inscricao in inscricoes_categoria:
            atletas_existentes = {inscricao.atleta1_id, inscricao.atleta2_id}
            if atletas_existentes == novos_atletas:
                flash("Essa dupla já está inscrita nesta categoria.", "error")
                return redirect(url_for("inscricoes.nova_inscricao_atleta", evento=evento_id))

        for inscricao in inscricoes_categoria:
            if (
                atleta_logado.id in [inscricao.atleta1_id, inscricao.atleta2_id] or
                parceiro.id in [inscricao.atleta1_id, inscricao.atleta2_id]
            ):
                flash("Um dos atletas já está inscrito para competir nesta categoria.", "error")
                return redirect(url_for("inscricoes.nova_inscricao_atleta", evento=evento_id))

        atletas_pendentes = []

        if not atleta_logado.nivel_validado:
            atletas_pendentes.append(atleta_logado.nome)

        if not parceiro.nivel_validado:
            atletas_pendentes.append(parceiro.nome)

        nova = Inscricao(
            atleta1_id=atleta_logado.id,
            atleta2_id=parceiro.id,
            categoria_id=categoria_id,
            status="confirmada"
        )

        db.session.add(nova)
        db.session.commit()

        flash("Inscrição realizada com sucesso!", "success")

        if atletas_pendentes:
            nomes = ", ".join(atletas_pendentes)
            flash(
                f"Atenção: a inscrição foi realizada, mas o nível do(s) atleta(s) {nomes} ainda não foi validado.",
                "error"
            )

        return redirect(url_for("inscricoes.minhas_inscricoes"))

    return render_template(
        "nova_inscricao_atleta.html",
        atleta_logado=atleta_logado,
        atletas=atletas,
        eventos=eventos,
        categorias=categorias,
        selected_evento_id=int(selected_evento_id)
    )