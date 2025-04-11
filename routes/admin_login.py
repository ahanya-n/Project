from flask import Blueprint, render_template, request, redirect, session

admin_login_bp = Blueprint('admin_login_bp', __name__)

# Hardcoded login credentials
ADMIN_EMAIL = "admin_gah@gmail.com"
ADMIN_PASSWORD = "Qwert@1234"

@admin_login_bp.route('/admin_login_page', methods=['GET'])
def admin_login_page():
    return render_template("admin_login.html")

@admin_login_bp.route('/admin_login', methods=['POST'])
def admin_login():
    email = request.form.get("email")
    password = request.form.get("password")

    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        session["admin_logged_in"] = True
        return redirect("/admin_dashboard")
    else:
        return render_template("error.html", message="✗ Invalid login credentials.")
