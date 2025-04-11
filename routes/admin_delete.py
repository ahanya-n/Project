from flask import Blueprint, render_template, request, redirect, session
from supabase import create_client

admin_delete_bp = Blueprint('admin_delete_bp', __name__)

url = "https://emocnhuvsjfwhyugadiq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtb2NuaHV2c2pmd2h5dWdhZGlxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM4NzU5ODksImV4cCI6MjA1OTQ1MTk4OX0.9RaSAKStvv4x4V1MyIaos92eXu-5FCwN3xJH1BRoyJk"
supabase = create_client(url, key)

@admin_delete_bp.route('/delete-product', methods=['GET', 'POST'])
def delete_product():
    if "admin_logged_in" not in session:
        return redirect('/admin_login_page')

    if request.method == 'POST':
        try:
            product_name = request.form.get('product_name')

            if not product_name:
                return render_template("error.html", message="✗ Product name required.")

            product_data = supabase.table("products").select("id").eq("name", product_name).execute().data
            if not product_data:
                return render_template("error.html", message="✗ Product not found.")

            product_id = product_data[0]["id"]

            # Delete from product_images
            supabase.table("product_images").delete().eq("product_id", product_id).execute()

            # Delete from products
            supabase.table("products").delete().eq("id", product_id).execute()

            return render_template("success.html", message="✓ Product and its images deleted successfully!")

        except Exception as e:
            return render_template("error.html", message=f"✗ Error: {e}")

    else:
        # Coming from dashboard with query param
        product_name = request.args.get("product_name")
        return render_template("admin_delete.html", product_name=product_name)
