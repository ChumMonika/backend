"""
WSGI Entry Point for DigitalOcean App Platform
Production-ready entry point with no side effects on import
"""
import os
from app import create_app

# Force production environment
os.environ.setdefault('FLASK_ENV', 'production')

# Create the application instance
app = create_app('production')

if __name__ == "__main__":
    # This block won't execute in gunicorn, but useful for testing
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
