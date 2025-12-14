"""
Simple test script to verify ZKP implementation
"""
from auth.crypto_utils import generate_keypair, point_multiply, point_to_dict, dict_to_point
from auth.schnorr_auth import SchnorrZKP

def test_zkp():
    """Test ZKP generation and verification"""
    print("=" * 60)
    print("Testing ZKP Implementation")
    print("=" * 60)
    
    # Generate key pair
    private_key, public_key = generate_keypair()
    print(f"\n1. Generated key pair:")
    print(f"   Private key: {hex(private_key)}")
    print(f"   Public key: x={hex(public_key.x)}, y={hex(public_key.y)}")
    
    # Generate proof
    proof = SchnorrZKP.generate_proof(private_key, public_key)
    print(f"\n2. Generated proof:")
    print(f"   R: x={proof['R']['x']}, y={proof['R']['y']}")
    print(f"   s: {proof['s']}")
    print(f"   c: {proof['c']}")
    
    # Verify proof
    is_valid = SchnorrZKP.verify_proof(proof, public_key)
    print(f"\n3. Verification result: {'VALID' if is_valid else 'INVALID'}")
    
    print("\n" + "=" * 60)
    return is_valid

if __name__ == '__main__':
    test_zkp()

