"""
General API routes
"""
from flask import Blueprint, jsonify, session, render_template
from auth.session_manager import SessionManager

api_bp = Blueprint('api', __name__)
session_manager = SessionManager()


@api_bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@api_bp.route('/api/status', methods=['GET'])
def status():
    """API status endpoint"""
    return jsonify({
        "status": "online",
        "protocol": "Schnorr Zero-Knowledge Proof",
        "version": "1.0.0"
    }), 200


