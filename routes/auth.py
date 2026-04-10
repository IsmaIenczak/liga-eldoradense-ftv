from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import Usuario

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

        session["usuario_id"] = usuario.id
        session["usuario_tipo"] = usuario.tipo

        flash("Login realizado com sucesso!", "success")
        return redirect(url_for("home"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for("auth.login"))