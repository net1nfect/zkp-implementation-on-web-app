"""
Authentication routes for ZKP Schnorr protocol
"""
from flask import Blueprint, request, jsonify, session, render_template
from models.user import User, get_db
from auth.schnorr_auth import SchnorrZKP
from auth.session_manager import SessionManager
from auth.crypto_utils import dict_to_point
from sqlalchemy.orm import Session

auth_bp = Blueprint('auth', __name__)
session_manager = SessionManager()


@auth_bp.route('/register', methods=['GET'])
def register_page():
    """Render registration page"""
    return render_template('register.html')


@auth_bp.route('/api/register', methods=['POST'])
def register():
    """
    Register a new user with their public key
    
    Expected JSON:
    {
        "username": "user123",
        "public_key": {
            "x": "0x...",
            "y": "0x..."
        }
    }
    """
    try:
        data = request.get_json()
        username = data.get('username')
        public_key = data.get('public_key')
        
        if not username or not public_key:
            return jsonify({"error": "Username and public_key are required"}), 400
        
        # Validate public key format
        if 'x' not in public_key or 'y' not in public_key:
            return jsonify({"error": "Invalid public key format"}), 400
        
        db: Session = next(get_db())
        
        # Check if username already exists
        existing_user = db.query(User).filter_by(username=username).first()
        if existing_user:
            db.close()
            return jsonify({"error": "Username already exists"}), 400
        
        # Create new user
        new_user = User(
            username=username,
            public_key_x=public_key['x'],
            public_key_y=public_key['y']
        )
        
        db.add(new_user)
        db.commit()
        user_id = new_user.id
        db.close()
        
        return jsonify({
            "message": "Registration successful",
            "user_id": user_id,
            "username": username
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/login', methods=['GET'])
def login_page():
    """Render login page"""
    return render_template('login.html')


@auth_bp.route('/api/login', methods=['POST'])
def login():
    """
    Authenticate user using Schnorr ZKP
    
    Expected JSON:
    {
        "username": "user123",
        "proof": {
            "R": {"x": "0x...", "y": "0x..."},
            "s": "0x...",
            "c": "0x..."
        }
    }
    """
    try:
        data = request.get_json()
        username = data.get('username')
        proof = data.get('proof')
        
        if not username or not proof:
            return jsonify({"error": "Username and proof are required"}), 400
        
        db: Session = next(get_db())
        
        # Get user from database
        user = db.query(User).filter_by(username=username).first()
        if not user:
            db.close()
            return jsonify({"error": "User not found"}), 404
        
        # Get public key
        public_key = user.get_public_key_point()
        
        # Debug: Print public key from database
        print(f"DEBUG: Public key from DB - x: {hex(public_key.x)}, y: {hex(public_key.y)}")
        print(f"DEBUG: Proof received - R: {proof.get('R')}, s: {proof.get('s')}, c: {proof.get('c')}")
        
        # Verify proof
        is_valid = SchnorrZKP.verify_proof(proof, public_key)
        
        if not is_valid:
            # Additional debug info
            print(f"DEBUG: Proof verification failed")
            db.close()
            return jsonify({"error": "Invalid proof"}), 401
        
        # Create session
        session_token = session_manager.create_session(str(user.id), username)
        
        # Store in Flask session
        session['user_id'] = user.id
        session['username'] = username
        session['session_token'] = session_token
        
        db.close()
        
        return jsonify({
            "message": "Login successful",
            "session_token": session_token,
            "user": {
                "id": user.id,
                "username": username
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    """Logout user and invalidate session"""
    session_token = session.get('session_token')
    if session_token:
        session_manager.invalidate_session(session_token)
    
    session.clear()
    return jsonify({"message": "Logout successful"}), 200


@auth_bp.route('/api/verify-session', methods=['GET'])
def verify_session():
    """Verify if current session is valid"""
    session_token = session.get('session_token')
    if not session_token:
        return jsonify({"authenticated": False}), 401
    
    session_data = session_manager.get_session(session_token)
    if not session_data:
        session.clear()
        return jsonify({"authenticated": False}), 401
    
    return jsonify({
        "authenticated": True,
        "user": {
            "id": session.get('user_id'),
            "username": session.get('username')
        }
    }), 200


