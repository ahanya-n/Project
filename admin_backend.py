from flask import Flask
from supabase import create_client
from routes.admin_dashboard import admin_dashboard_bp
from routes.admin_upload import admin_upload_bp
from routes.admin_modify import admin_modify_bp
from routes.admin_delete import admin_delete_bp


# Initialize Flask app
app = Flask(__name__)
app.secret_key = "myS3cr3t!123"

# Supabase setup
url = "https://emocnhuvsjfwhyugadiq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtb2NuaHV2c2pmd2h5dWdhZGlxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM4NzU5ODksImV4cCI6MjA1OTQ1MTk4OX0.9RaSAKStvv4x4V1MyIaos92eXu-5FCwN3xJH1BRoyJk"
supabase = create_client(url, key)

# Register all blueprints
from routes.home import home_bp
from routes.admin_login import admin_login_bp
from routes.admin_dashboard import admin_dashboard_bp
from routes.admin_upload import admin_upload_bp
from routes.admin_modify import admin_modify_bp
from routes.admin_delete import admin_delete_bp

app.register_blueprint(home_bp)
app.register_blueprint(admin_login_bp)
app.register_blueprint(admin_dashboard_bp)
app.register_blueprint(admin_upload_bp)
app.register_blueprint(admin_modify_bp)
app.register_blueprint(admin_delete_bp)

# Run the main app
if __name__ == '__main__':
    app.run(debug=True)
