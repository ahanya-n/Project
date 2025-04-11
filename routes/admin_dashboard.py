from flask import Blueprint, render_template, request, session, redirect
from supabase import create_client
import base64

admin_dashboard_bp = Blueprint('admin_dashboard_bp', __name__)

# Supabase connection
url = "https://emocnhuvsjfwhyugadiq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtb2NuaHV2c2pmd2h5dWdhZGlxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM4NzU5ODksImV4cCI6MjA1OTQ1MTk4OX0.9RaSAKStvv4x4V1MyIaos92eXu-5FCwN3xJH1BRoyJk"
supabase = create_client(url, key)

@admin_dashboard_bp.route('/admin_dashboard')
def admin_dashboard():
    if "admin_logged_in" not in session:
        return redirect('/admin_login_page')
    return render_template("admin_dashboard.html", products=[])

@admin_dashboard_bp.route('/search_product')
def search_product():
    if "admin_logged_in" not in session:
        return redirect('/admin_login_page')

    query = request.args.get('query', '').strip()
    if not query:
        return render_template("admin_dashboard.html", products=[])

    # Search product by name
    products = supabase.table("products").select("*").ilike("name", f"%{query}%").execute().data or []

    # Load one image per product (base64)
    for product in products:
        image_data = supabase.table("product_images").select("image").eq("product_id", product["id"]).limit(1).execute().data
        if image_data:
            product["image"] = image_data[0]["image"]
        else:
            product["image"] = None

    return render_template("admin_dashboard.html", products=products)
