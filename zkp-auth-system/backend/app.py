"""
Main Flask application for ZKP Authentication System
"""
from flask import Flask
from routes.auth_routes import auth_bp
from routes.api_routes import api_bp
from config import SECRET_KEY, DEBUG

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['DEBUG'] = DEBUG

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)


@app.errorhandler(404)
def not_found(error):
    return {"error": "Not found"}, 404


@app.errorhandler(500)
def internal_error(error):
    return {"error": "Internal server error"}, 500


if __name__ == '__main__':
    print("=" * 60)
    print("ZKP Authentication System - Schnorr Protocol")
    print("=" * 60)
    print("Server starting on http://localhost:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)


