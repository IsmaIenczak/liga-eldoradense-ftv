from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import Usuario, Atleta, Nivel
from extensions import db
from utils import senha_forte, normalizar_telefone, normalizar_cpf


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario or not usuario.check_senha(senha):
            flash("Email ou senha inválidos.", "error")
            return redirect(url_for("auth.login"))

        session.permanent = True
        session["usuario_id"] = usuario.id
        session["usuario_tipo"] = usuario.tipo
        session["atleta_id"] = usuario.atleta_id

        flash("Login realizado com sucesso!", "success")
        return redirect(url_for("home"))

    return render_template("login.html")



@auth_bp.route("/cadastro-atleta", methods=["GET", "POST"])
def cadastro_atleta():
    niveis = Nivel.query.order_by(Nivel.nome.asc()).all()

    if request.method == "POST":
        nome = request.form.get("nome")

        cpf = normalizar_cpf(request.form.get("cpf"))
        if cpf is None:
            flash("Informe um CPF válido com 11 números.", "error")
            return redirect(url_for("auth.cadastro_atleta"))

        telefone = request.form.get("telefone")
        telefone = normalizar_telefone(telefone)
        sexo = request.form.get("sexo")
        if telefone is None:
            flash("Informe um telefone válido com DDD.", "error")
            return redirect(url_for("auth.cadastro_atleta"))
        nivel_id = request.form.get("nivel")
        residente_eldorado = request.form.get("residente_eldorado")
        email = request.form.get("email")
        senha = request.form.get("senha")
        confirmar_senha = request.form.get("confirmar_senha")

        residente_eldorado = True if residente_eldorado == "sim" else False

        if not cpf or not cpf.isdigit() or len(cpf) != 11:
            flash("Informe um CPF válido com 11 números.", "error")
            return redirect(url_for("auth.cadastro_atleta"))

        if not email or not email.strip():
            flash("Informe um email válido.", "error")
            return redirect(url_for("auth.cadastro_atleta"))

        if not senha_forte(senha):
            flash(
                "A senha deve ter pelo menos 8 caracteres, incluindo 1 letra maiúscula, 1 número e 1 caractere especial.",
                "error"
            )
            return redirect(url_for("auth.cadastro_atleta"))

        if senha != confirmar_senha:
            flash("A confirmação de senha não confere.", "error")
            return redirect(url_for("auth.cadastro_atleta"))

        usuario_existente_email = Usuario.query.filter_by(email=email.strip()).first()
        if usuario_existente_email:
            flash("Já existe um usuário cadastrado com esse email.", "error")
            return redirect(url_for("auth.cadastro_atleta"))

        atleta = Atleta.query.filter_by(cpf=cpf).first()

        if atleta:
            usuario_existente_atleta = Usuario.query.filter_by(atleta_id=atleta.id).first()
            if usuario_existente_atleta:
                flash("Este atleta já possui uma conta de acesso cadastrada.", "error")
                return redirect(url_for("auth.cadastro_atleta"))
        else:
            if not nome or not nome.strip():
                flash("Informe um nome válido.", "error")
                return redirect(url_for("auth.cadastro_atleta"))

            if sexo not in ["masculino", "feminino"]:
                flash("Informe um sexo válido.", "error")
                return redirect(url_for("auth.cadastro_atleta"))

            if not nivel_id:
                flash("Selecione um nível.", "error")
                return redirect(url_for("auth.cadastro_atleta"))


            atleta = Atleta(
            nome=nome.strip(),
            cpf=cpf,
            sexo=sexo,
            nivel_id=int(nivel_id),
            residente_eldorado=residente_eldorado,
            nivel_validado=False,
            telefone=telefone
            )

            db.session.add(atleta)
            db.session.flush()

        usuario = Usuario(
            email=email.strip(),
            tipo="atleta",
            atleta_id=atleta.id
        )
        usuario.set_senha(senha)

        db.session.add(usuario)
        db.session.commit()

        flash("Conta de atleta criada com sucesso! Agora faça login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("cadastro_atleta.html", niveis=niveis)



    
@auth_bp.route("/primeiro-acesso", methods=["GET", "POST"])
def primeiro_acesso():
    if request.method == "POST":
        etapa = request.form.get("etapa")

        if etapa == "buscar":
            
            cpf = normalizar_cpf(request.form.get("cpf"))
            if cpf is None:
                flash("Informe um CPF válido com 11 números.", "error")
                return redirect(url_for("auth.primeiro_acesso"))

            if not cpf or not cpf.isdigit() or len(cpf) != 11:
                flash("Informe um CPF válido com 11 números.", "error")
                return redirect(url_for("auth.primeiro_acesso"))

            atleta = Atleta.query.filter_by(cpf=cpf).first()

            if not atleta:
                flash("Nenhum atleta cadastrado foi encontrado com esse CPF.", "error")
                return redirect(url_for("auth.primeiro_acesso"))

            if atleta.usuario:
                flash("Este atleta já possui conta de acesso. Faça login.", "error")
                return redirect(url_for("auth.login"))

            return render_template("primeiro_acesso.html", atleta=atleta, etapa="completar")

        elif etapa == "completar":
            atleta_id = request.form.get("atleta_id")
            telefone = normalizar_telefone(request.form.get("telefone"))
            if telefone is None:
                flash("Informe um telefone válido com DDD.", "error")
                return render_template("primeiro_acesso.html", atleta=atleta, etapa="completar")
            email = request.form.get("email")
            senha = request.form.get("senha")
            confirmar_senha = request.form.get("confirmar_senha")

            atleta = Atleta.query.get(atleta_id)

            if not atleta:
                flash("Atleta não encontrado.", "error")
                return redirect(url_for("auth.primeiro_acesso"))

            if atleta.usuario:
                flash("Este atleta já possui conta de acesso. Faça login.", "error")
                return redirect(url_for("auth.login"))

            if not email or not email.strip():
                flash("Informe um email válido.", "error")
                return render_template("primeiro_acesso.html", atleta=atleta, etapa="completar")

            usuario_existente_email = Usuario.query.filter_by(email=email.strip()).first()
            if usuario_existente_email:
                flash("Já existe um usuário cadastrado com esse email.", "error")
                return render_template("primeiro_acesso.html", atleta=atleta, etapa="completar")

            if not senha_forte(senha):
                flash(
                    "A senha deve ter pelo menos 8 caracteres, incluindo 1 letra maiúscula, 1 número e 1 caractere especial.",
                    "error"
                )
                return render_template("primeiro_acesso.html", atleta=atleta, etapa="completar")

            if senha != confirmar_senha:
                flash("A confirmação de senha não confere.", "error")
                return render_template("primeiro_acesso.html", atleta=atleta, etapa="completar")

            atleta.telefone = telefone

            usuario = Usuario(
                email=email.strip(),
                tipo="atleta",
                atleta_id=atleta.id
            )
            usuario.set_senha(senha)

            db.session.add(usuario)
            db.session.commit()

            flash("Primeiro acesso concluído com sucesso! Agora faça login.", "success")
            return redirect(url_for("auth.login"))

    return render_template("primeiro_acesso.html", etapa="buscar")



@auth_bp.route("/meu-perfil", methods=["GET", "POST"])
def meu_perfil():
    if session.get("usuario_tipo") != "atleta":
        flash("Acesso permitido apenas para atletas.", "error")
        return redirect(url_for("home"))

    atleta_id = session.get("atleta_id")
    if not atleta_id:
        return redirect(url_for("auth.logout"))

    atleta = Atleta.query.get(atleta_id)
    if not atleta or not atleta.usuario:
        return redirect(url_for("auth.logout"))

    if request.method == "POST":
        telefone = normalizar_telefone(request.form.get("telefone"))
        if telefone is None:
            flash("Informe um telefone válido com DDD.", "error")
            return redirect(url_for("auth.meu_perfil"))
        email = request.form.get("email")

        if not email or not email.strip():
            flash("Informe um email válido.", "error")
            return redirect(url_for("auth.meu_perfil"))

        email = email.strip()

        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente and usuario_existente.id != atleta.usuario.id:
            flash("Já existe outro usuário cadastrado com esse email.", "error")
            return redirect(url_for("auth.meu_perfil"))

        atleta.telefone = telefone
        atleta.usuario.email = email

        db.session.commit()

        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for("auth.meu_perfil"))

    return render_template("meu_perfil.html", atleta=atleta)


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for("auth.login"))