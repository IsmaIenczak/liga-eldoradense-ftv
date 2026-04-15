from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import Usuario, Atleta, Nivel
from extensions import db
from utils import senha_forte

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
        cpf = request.form.get("cpf")
        telefone = request.form.get("telefone")
        sexo = request.form.get("sexo")
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


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for("auth.login"))