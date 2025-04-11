from flask import Blueprint, render_template, request, session, redirect
from supabase import create_client
import base64
import re

admin_modify_bp = Blueprint('admin_modify_bp', __name__)

url = "https://emocnhuvsjfwhyugadiq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtb2NuaHV2c2pmd2h5dWdhZGlxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM4NzU5ODksImV4cCI6MjA1OTQ1MTk4OX0.9RaSAKStvv4x4V1MyIaos92eXu-5FCwN3xJH1BRoyJk"
supabase = create_client(url, key)

@admin_modify_bp.route('/admin_modify', methods=['GET', 'POST'])
def admin_modify():
    if "admin_logged_in" not in session:
        return redirect('/admin_login_page')

    if request.method == 'POST':
        try:
            product_name = request.form.get('product_name')
            column = request.form.get('column')

            if not product_name or not column:
                return render_template("error.html", message="✗ Missing fields")

            product_res = supabase.table("products").select("id").eq("name", product_name).execute()
            if not product_res.data:
                return render_template("error.html", message="✗ Product not found.")

            product_id = product_res.data[0]['id']

            if column == "image":
                image_file = request.files.get("image")
                if image_file and image_file.filename:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')
                    supabase.table("product_images").insert({
                        "product_id": product_id,
                        "image": image_data
                    }).execute()
                return render_template("success.html", message="✓ Image added!")

            else:
                new_value = request.form.get('new_value')
                if not new_value:
                    return render_template("error.html", message="✗ Missing new value")

                if column == "price":
                    new_value = float(re.sub(r"[^\d.]", "", new_value))
                    if new_value > 99999999.99:
                        return render_template("error.html", message="✗ Price too high")

                supabase.table("products").update({column: new_value}).eq("id", product_id).execute()
                return render_template("success.html", message="✓ Product updated!")

        except Exception as e:
            return render_template("error.html", message=f"✗ Error: {e}")

    else:
        product_name = request.args.get("product_name")
        images = []
        if product_name:
            product = supabase.table("products").select("id").eq("name", product_name).execute().data
            if product:
                product_id = product[0]["id"]
                images = supabase.table("product_images").select("image").eq("product_id", product_id).execute().data

        return render_template("admin_modify.html", product_name=product_name, images=images)