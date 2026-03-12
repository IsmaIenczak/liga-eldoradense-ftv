from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from extensions import db
from models import Atleta, Evento, Categoria, Inscricao

inscricoes_bp = Blueprint("inscricoes", __name__)




@inscricoes_bp.route("/api/eventos/<int:evento_id>/categorias")
def api_categorias_por_evento(evento_id):
    categorias = Categoria.query.filter_by(evento_id=evento_id).all()

    return jsonify([
        {
            "id": c.id,
            "nome": c.nome,
            "nivel": c.nivel,
            "modalidade": c.modalidade,
            "vagas": c.vagas,
            "inscritos": len(c.inscricoes),
            "vagas_restantes": c.vagas - len(c.inscricoes),
            "lotada": len(c.inscricoes) >= c.vagas
        }
        for c in categorias
    ])




@inscricoes_bp.route("/inscricoes/nova", methods=["GET", "POST"])
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

        if categoria.evento_id != int(evento_id):
            flash("A categoria selecionada não pertence ao evento escolhido.", "error")
            return redirect(url_for("inscricoes.nova_inscricao", evento=evento_id))

        if atleta1_id == atleta2_id:
            flash("Selecione atletas diferentes", "error")
            return redirect(url_for("inscricoes.nova_inscricao", evento=evento_id))

        if atleta1.nivel.strip().lower() != atleta2.nivel.strip().lower():
            flash("Os atletas devem estar no mesmo nível", "error")
            return redirect(url_for("inscricoes.nova_inscricao", evento=evento_id))

        if categoria.nivel.strip().lower() != atleta1.nivel.strip().lower():
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

        nova = Inscricao(
            atleta1_id=atleta1_id,
            atleta2_id=atleta2_id,
            categoria_id=categoria_id
        )

        db.session.add(nova)
        db.session.commit()

        flash("Inscrição realizada com sucesso!", "success")
        return redirect(url_for("inscricoes.nova_inscricao", evento=evento_id))

    return render_template(
        "nova_inscricao.html",
        atletas=atletas,
        eventos=eventos,
        categorias=categorias,
        selected_evento_id=int(selected_evento_id)
    )


#Rota de listagem de inscrições
@inscricoes_bp.route("/inscricoes")
def listar_inscricoes():
    inscricoes = Inscricao.query.all()
    return render_template("inscricoes.html", inscricoes=inscricoes)



#Rota dinâmica para exclusão de inscrição
@inscricoes_bp.route("/inscricoes/excluir/<int:inscricao_id>", methods=["POST"])
def excluir_inscricao(inscricao_id):
    inscricao = Inscricao.query.get_or_404(inscricao_id)

    db.session.delete(inscricao)
    db.session.commit()

    flash("Inscrição excluída com sucesso!", "success")
    return redirect(url_for("inscricoes.listar_inscricoes"))