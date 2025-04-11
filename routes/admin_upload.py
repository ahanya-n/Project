from flask import Blueprint, render_template, request, redirect, session
from supabase import create_client
import base64
import random

admin_upload_bp = Blueprint('admin_upload_bp', __name__)

url = "https://emocnhuvsjfwhyugadiq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtb2NuaHV2c2pmd2h5dWdhZGlxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM4NzU5ODksImV4cCI6MjA1OTQ1MTk4OX0.9RaSAKStvv4x4V1MyIaos92eXu-5FCwN3xJH1BRoyJk"
supabase = create_client(url, key)

def generate_unique_id():
    used_ids = supabase.table("products").select("id").execute().data
    used = set([int(item["id"]) for item in used_ids if str(item["id"]).isdigit()])
    available = [str(i) for i in range(1, 1001) if i not in used]
    return random.choice(available) if available else None


@admin_upload_bp.route('/upload-product')
def upload_form():
    if "admin_logged_in" not in session:
        return redirect('/admin_login_page')
    return render_template("admin_upload.html")

@admin_upload_bp.route('/upload', methods=['POST'])
def upload_product():
    if "admin_logged_in" not in session:
        return redirect('/admin_login_page')

    try:
        product_id = generate_unique_id()
        if not product_id:
            return render_template("error.html", message="✗ No ID available.")

        name = request.form['product_title']
        price = request.form['price'].replace('₹', '').replace(',', '').strip()
        description = request.form['description']
        files = request.files.getlist('images')

        supabase.table("products").insert({
            "id": product_id,
            "name": name,
            "price": float(price),
            "description": description
        }).execute()

        for file in files:
            if file.filename:
                image_bytes = file.read()
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                supabase.table("product_images").insert({
                    "product_id": product_id,
                    "image": image_base64
                }).execute()

        return render_template("success.html", message="✓ Product uploaded successfully!")

    except Exception as e:
        return render_template("error.html", message=f"✗ Upload failed: {e}")
