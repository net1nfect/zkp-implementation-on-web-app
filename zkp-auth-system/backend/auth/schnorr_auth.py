"""
Schnorr Zero-Knowledge Proof Authentication Implementation
"""
from typing import Tuple, Dict, Optional
from config import CURVE_N
from auth.crypto_utils import (
    Point, G, point_multiply, hash_to_int, point_add,
    generate_keypair, point_to_dict, dict_to_point
)
import secrets


class SchnorrZKP:
    """
    Schnorr Zero-Knowledge Proof Protocol
    
    Protocol:
    1. Prover generates random r, computes R = r*G, sends R to Verifier
    2. Verifier generates random challenge c, sends to Prover
    3. Prover computes s = r + c*x (mod n), sends s to Verifier
    4. Verifier checks: s*G == R + c*Y
    
    Where:
    - x = private key (secret)
    - Y = public key = x*G
    - r = random nonce
    - c = challenge
    - s = response
    """
    
    @staticmethod
    def generate_proof(private_key: int, public_key: Point) -> Dict:
        """
        Generate a Schnorr ZKP proof
        
        Args:
            private_key: The secret private key
            public_key: The public key point
            
        Returns:
            Dictionary containing proof components (R, s)
        """
        # Step 1: Generate random nonce r
        r = secrets.randbelow(CURVE_N - 1) + 1
        
        # Step 2: Compute R = r * G
        R = point_multiply(r, G)
        
        # Step 3: Generate challenge c = H(R || Y || message)
        # In authentication, message can be a timestamp or session ID
        message = "authentication"
        c = hash_to_int(R, public_key, message)
        
        # Step 4: Compute response s = r + c * x (mod n)
        s = (r + c * private_key) % CURVE_N
        
        return {
            "R": point_to_dict(R),
            "s": hex(s),
            "c": hex(c)
        }
    
    @staticmethod
    def verify_proof(proof: Dict, public_key: Point, message: str = "authentication") -> bool:
        """
        Verify a Schnorr ZKP proof
        
        Args:
            proof: Dictionary containing R, s, c
            public_key: The public key point
            message: The message used in challenge generation
            
        Returns:
            True if proof is valid, False otherwise
        """
        try:
            # Extract proof components
            R = dict_to_point(proof["R"])
            s = int(proof["s"], 16)
            c = int(proof["c"], 16)
            
            # Debug: Recalculate challenge to verify
            calculated_c = hash_to_int(R, public_key, message)
            print(f"DEBUG: Challenge from proof: {hex(c)}, Calculated: {hex(calculated_c)}")
            
            # Verify: s*G == R + c*Y
            left_side = point_multiply(s, G)
            
            # Compute c*Y
            cY = point_multiply(c, public_key)
            
            # Compute R + c*Y
            right_side = point_add(R, cY)
            
            # Debug: Print verification details
            print(f"DEBUG: left_side (s*G): x={hex(left_side.x)}, y={hex(left_side.y)}")
            print(f"DEBUG: right_side (R+c*Y): x={hex(right_side.x)}, y={hex(right_side.y)}")
            print(f"DEBUG: Verification result: {left_side == right_side}")
            
            # Check equality
            return left_side == right_side
            
        except (KeyError, ValueError, TypeError) as e:
            print(f"Proof verification error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    @staticmethod
    def generate_challenge(public_key: Point, R: Point, message: str = "authentication") -> int:
        """
        Generate challenge for interactive proof (if needed)
        
        Args:
            public_key: The public key point
            R: The commitment point
            message: Optional message
            
        Returns:
            Challenge value c
        """
        return hash_to_int(R, public_key, message)

