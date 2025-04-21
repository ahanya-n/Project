from flask import Blueprint, render_template, request, redirect, session
from supabase import create_client, Client

# Supabase credentials
url = "https://emocnhuvsjfwhyugadiq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtb2NuaHV2c2pmd2h5dWdhZGlxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM4NzU5ODksImV4cCI6MjA1OTQ1MTk4OX0.9RaSAKStvv4x4V1MyIaos92eXu-5FCwN3xJH1BRoyJk"
supabase: Client = create_client(url, key)

# Flask blueprint
admin_login_bp = Blueprint('admin_login_bp', __name__)

@admin_login_bp.route('/admin_login_page', methods=['GET'])
def admin_login_page():
    return render_template("admin_login.html")

@admin_login_bp.route('/admin_login', methods=['POST'])
def admin_login():
    email = request.form.get("email")
    password = request.form.get("password")

    # Query the admin table to verify credentials
    result = supabase.table("admin").select("*").eq("admin", email).eq("password", password).execute()

    if result.data and len(result.data) > 0:
        session["admin_logged_in"] = True
        return redirect("/admin_dashboard")
    else:
        return render_template("error.html", message="✗ Invalid login credentials.")