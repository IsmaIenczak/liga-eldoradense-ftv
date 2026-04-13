from functools import wraps
from flask import session, redirect, url_for, flash
import re


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