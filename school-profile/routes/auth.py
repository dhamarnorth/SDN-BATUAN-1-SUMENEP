"""Autentikasi admin.

- Login memakai username + password (password disimpan sebagai hash).
- Session Flask dipakai untuk menandai admin yang sedang login.
- Seluruh halaman dashboard dilindungi oleh routes/admin.py (before_request).
"""

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash

from db import fetch_one

bp = Blueprint("auth", __name__)


def load_logged_in_user(app):
    """Dipanggil sekali dari app.py: membaca session sebelum tiap request."""

    @app.before_request
    def _load_user():
        user_id = session.get("admin_id")
        if user_id is None:
            g.admin = None
        else:
            g.admin = fetch_one(
                "SELECT id, username, nama, role FROM users WHERE id = %s", (user_id,)
            )
            if g.admin is None:
                # user sudah dihapus di database -> paksa logout
                session.clear()

    return _load_user


@bp.route("/admin/login", methods=("GET", "POST"))
def login():
    # Kalau sudah login, langsung ke dashboard
    if g.get("admin") is not None:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username dan password wajib diisi.", "error")
        else:
            user = fetch_one("SELECT * FROM users WHERE username = %s", (username,))
            # password dibandingkan dengan hash, bukan teks biasa
            if user and check_password_hash(user["password"], password):
                session.clear()
                session["admin_id"] = user["id"]
                flash(f"Selamat datang, {user['nama']}!", "success")
                tujuan = request.args.get("next") or url_for("admin.dashboard")
                return redirect(tujuan)
            flash("Username atau password salah.", "error")

    return render_template("auth/login.html", title="Login Admin")


@bp.route("/admin/logout")
def logout():
    session.clear()
    flash("Anda sudah keluar dari dashboard.", "info")
    return redirect(url_for("public.index"))
