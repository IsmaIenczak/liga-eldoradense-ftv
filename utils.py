import re
from functools import wraps
from flask import session, redirect, url_for, flash


def admin_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if session.get("usuario_tipo") != "admin":
            flash("Acesso permitido apenas para administradores.", "error")
            return redirect(url_for("home"))

        return view_func(*args, **kwargs)

    return wrapped_view


def senha_forte(senha):
    if len(senha) < 8:
        return False

    if not re.search(r"[A-Z]", senha):
        return False

    if not re.search(r"[0-9]", senha):
        return False

    if not re.search(r"[^A-Za-z0-9]", senha):
        return False

    return True


def normalizar_telefone(telefone):
    if not telefone:
        return None

    telefone = telefone.strip()

    if re.search(r"[A-Za-z]", telefone):
        return None

    telefone_limpo = re.sub(r"\D", "", telefone)

    if len(telefone_limpo) not in [10, 11]:
        return None

    return telefone_limpo


def formatar_telefone(telefone):
    if not telefone:
        return "Não informado"

    telefone_limpo = re.sub(r"\D", "", telefone)

    if len(telefone_limpo) == 11:
        return f"({telefone_limpo[:2]}) {telefone_limpo[2:7]}-{telefone_limpo[7:]}"
    elif len(telefone_limpo) == 10:
        return f"({telefone_limpo[:2]}) {telefone_limpo[2:6]}-{telefone_limpo[6:]}"

    return telefone