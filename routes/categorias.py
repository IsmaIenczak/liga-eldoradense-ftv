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
        vagas = request.form.get("vagas")

        if not vagas or not vagas.isdigit():
            flash("O número de vagas deve ser um número inteiro válido.", "error")
            return redirect(url_for("categorias.nova_categoria"))

        vagas = int(vagas)

        if vagas < 4:
            flash("O número de vagas deve ser no mínimo 4.", "error")
            return redirect(url_for("categorias.nova_categoria"))

        if vagas % 2 != 0:
            flash("O número de vagas deve ser par.", "error")
            return redirect(url_for("categorias.nova_categoria"))

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
            vagas=vagas,
            evento_id=int(evento_id)
        )

        db.session.add(nova)
        db.session.commit()

        flash("Categoria criada com sucesso!", "success")
        return redirect(url_for("categorias.listar_categorias"))

    return render_template("nova_categoria.html", eventos=eventos)




@categorias_bp.route("/categorias")
def listar_categorias():
    categorias = Categoria.query.all()
    return render_template("categorias.html", categorias=categorias)




@categorias_bp.route("/categorias/excluir/<int:categoria_id>", methods=["POST"])
def excluir_categoria(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)

    if categoria.inscricoes:
        flash(
            "Esta categoria não pode ser excluída porque possui inscrições vinculadas.",
            "error"
        )
        return redirect(url_for("categorias.listar_categorias"))

    db.session.delete(categoria)
    db.session.commit()

    flash("Categoria excluída com sucesso!", "success")
    return redirect(url_for("categorias.listar_categorias"))



@categorias_bp.route("/categorias/editar/<int:categoria_id>", methods=["GET", "POST"])
def editar_categoria(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    eventos = Evento.query.all()

    if request.method == "POST":
        nova_modalidade = request.form.get("modalidade")
        novo_nivel = request.form.get("nivel")
        novo_evento_id = int(request.form.get("evento"))
        novas_vagas = request.form.get("vagas")

        if not novas_vagas or not novas_vagas.isdigit():
            flash("O número de vagas deve ser um número inteiro válido.", "error")
            return redirect(url_for("categorias.editar_categoria", categoria_id=categoria.id))

        novas_vagas = int(novas_vagas)

        if novas_vagas < 4:
            flash("O número de vagas deve ser no mínimo 4.", "error")
            return redirect(url_for("categorias.editar_categoria", categoria_id=categoria.id))

        if novas_vagas % 2 != 0:
            flash("O número de vagas deve ser par.", "error")
            return redirect(url_for("categorias.editar_categoria", categoria_id=categoria.id))

        quantidade_inscritos = len(categoria.inscricoes)
        if novas_vagas < quantidade_inscritos:
            flash(
                f"Não é possível definir {novas_vagas} vagas: a categoria já possui {quantidade_inscritos} inscrições.",
                "error"
            )
            return redirect(url_for("categorias.editar_categoria", categoria_id=categoria.id))

        categoria_tem_inscricoes = len(categoria.inscricoes) > 0

        if categoria_tem_inscricoes:
            if novo_evento_id != categoria.evento_id:
                flash(
                    "Não é possível alterar o evento de uma categoria que já possui inscrições.",
                    "error"
                )
                return redirect(url_for("categorias.editar_categoria", categoria_id=categoria.id))

            for inscricao in categoria.inscricoes:
                atleta1 = inscricao.atleta1
                atleta2 = inscricao.atleta2

                sexo1 = atleta1.sexo.strip().lower()
                sexo2 = atleta2.sexo.strip().lower()
                nivel1 = atleta1.nivel.strip().lower()
                nivel2 = atleta2.nivel.strip().lower()

                nova_modalidade_normalizada = nova_modalidade.strip().lower()
                novo_nivel_normalizado = novo_nivel.strip().lower()

                if nivel1 != novo_nivel_normalizado or nivel2 != novo_nivel_normalizado:
                    flash(
                        f"Não é possível alterar esta categoria: a inscrição da dupla {atleta1.nome} e {atleta2.nome} ficaria com nível incompatível.",
                        "error"
                    )
                    return redirect(url_for("categorias.editar_categoria", categoria_id=categoria.id))

                if nova_modalidade_normalizada == "masculino":
                    if sexo1 != "masculino" or sexo2 != "masculino":
                        flash(
                            f"Não é possível alterar esta categoria: a dupla {atleta1.nome} e {atleta2.nome} não se encaixa em categoria masculina.",
                            "error"
                        )
                        return redirect(url_for("categorias.editar_categoria", categoria_id=categoria.id))

                elif nova_modalidade_normalizada == "feminino":
                    if sexo1 != "feminino" or sexo2 != "feminino":
                        flash(
                            f"Não é possível alterar esta categoria: a dupla {atleta1.nome} e {atleta2.nome} não se encaixa em categoria feminina.",
                            "error"
                        )
                        return redirect(url_for("categorias.editar_categoria", categoria_id=categoria.id))

                elif nova_modalidade_normalizada == "misto":
                    if sexo1 == sexo2:
                        flash(
                            f"Não é possível alterar esta categoria: a dupla {atleta1.nome} e {atleta2.nome} deixaria de se encaixar em categoria mista.",
                            "error"
                        )
                        return redirect(url_for("categorias.editar_categoria", categoria_id=categoria.id))

        categoria_existente = Categoria.query.filter_by(
            evento_id=novo_evento_id,
            modalidade=nova_modalidade,
            nivel=novo_nivel
        ).first()

        if categoria_existente and categoria_existente.id != categoria.id:
            flash("Já existe uma categoria com essa modalidade e nível neste evento.", "error")
            return redirect(url_for("categorias.editar_categoria", categoria_id=categoria.id))

        categoria.modalidade = nova_modalidade
        categoria.nivel = novo_nivel
        categoria.vagas = novas_vagas
        categoria.evento_id = novo_evento_id

        db.session.commit()

        flash("Categoria atualizada com sucesso!", "success")
        return redirect(url_for("categorias.listar_categorias"))

    return render_template("editar_categoria.html", categoria=categoria, eventos=eventos)