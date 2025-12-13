"""
Session management for authenticated users
"""
from datetime import datetime, timedelta
from typing import Optional, Dict
import secrets


class SessionManager:
    """Manages user sessions and authentication state"""
    
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
        self.session_timeout = timedelta(hours=1)
    
    def create_session(self, user_id: str, username: str) -> str:
        """
        Create a new session for authenticated user
        
        Args:
            user_id: Unique user identifier
            username: Username
            
        Returns:
            Session token
        """
        session_token = secrets.token_urlsafe(32)
        self.sessions[session_token] = {
            "user_id": user_id,
            "username": username,
            "created_at": datetime.now(),
            "last_activity": datetime.now()
        }
        return session_token
    
    def get_session(self, session_token: str) -> Optional[Dict]:
        """
        Get session data if valid
        
        Args:
            session_token: Session token
            
        Returns:
            Session data or None if invalid/expired
        """
        if session_token not in self.sessions:
            return None
        
        session = self.sessions[session_token]
        
        # Check if session expired
        if datetime.now() - session["last_activity"] > self.session_timeout:
            del self.sessions[session_token]
            return None
        
        # Update last activity
        session["last_activity"] = datetime.now()
        return session
    
    def invalidate_session(self, session_token: str) -> bool:
        """
        Invalidate a session
        
        Args:
            session_token: Session token to invalidate
            
        Returns:
            True if session was found and invalidated
        """
        if session_token in self.sessions:
            del self.sessions[session_token]
            return True
        return False
    
    def cleanup_expired_sessions(self):
        """Remove all expired sessions"""
        now = datetime.now()
        expired = [
            token for token, session in self.sessions.items()
            if now - session["last_activity"] > self.session_timeout
        ]
        for token in expired:
            del self.sessions[token]


