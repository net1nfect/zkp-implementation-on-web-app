"""
Cryptographic utilities for Schnorr Zero-Knowledge Proof
"""
import hashlib
import secrets
from typing import Tuple
from config import CURVE_P, CURVE_N, CURVE_G_X, CURVE_G_Y


class Point:
    """Elliptic curve point representation"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return f"Point({hex(self.x)}, {hex(self.y)})"


# Generator point G
G = Point(CURVE_G_X, CURVE_G_Y)


def mod_inverse(a: int, m: int) -> int:
    """Calculate modular inverse using Extended Euclidean Algorithm"""
    if a < 0:
        a = a % m
    return pow(a, -1, m)


def point_add(p1: Point, p2: Point) -> Point:
    """Add two points on the elliptic curve"""
    # Handle point at infinity
    if p1.x == 0 and p1.y == 0:
        return p2
    if p2.x == 0 and p2.y == 0:
        return p1
    
    if p1.x == p2.x and p1.y == p2.y:
        # Point doubling
        if p1.y == 0:
            return Point(0, 0)  # Point at infinity
        s = (3 * p1.x * p1.x) * mod_inverse(2 * p1.y, CURVE_P) % CURVE_P
    else:
        # Point addition
        if p1.x == p2.x:
            return Point(0, 0)  # Point at infinity
        s = (p2.y - p1.y) * mod_inverse(p2.x - p1.x, CURVE_P) % CURVE_P
    
    x3 = (s * s - p1.x - p2.x) % CURVE_P
    y3 = (s * (p1.x - x3) - p1.y) % CURVE_P
    
    # Ensure positive modulo
    if x3 < 0:
        x3 = x3 + CURVE_P
    if y3 < 0:
        y3 = y3 + CURVE_P
    
    return Point(x3 % CURVE_P, y3 % CURVE_P)


def point_multiply(k: int, point: Point) -> Point:
    """Scalar multiplication: k * point"""
    if k == 0:
        return Point(0, 0)  # Point at infinity
    
    result = Point(0, 0)  # Identity point
    addend = point
    
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    
    return result


def hash_to_int(*args) -> int:
    """Hash multiple values and convert to integer"""
    h = hashlib.sha256()
    for arg in args:
        if isinstance(arg, int):
            h.update(arg.to_bytes(32, 'big'))
        elif isinstance(arg, Point):
            h.update(arg.x.to_bytes(32, 'big'))
            h.update(arg.y.to_bytes(32, 'big'))
        else:
            h.update(str(arg).encode())
    return int(h.hexdigest(), 16) % CURVE_N


def generate_keypair() -> Tuple[int, Point]:
    """
    Generate a private/public key pair for Schnorr protocol
    
    Returns:
        Tuple of (private_key, public_key_point)
    """
    private_key = secrets.randbelow(CURVE_N - 1) + 1  # 1 to N-1
    public_key = point_multiply(private_key, G)
    return private_key, public_key


def point_to_dict(point: Point) -> dict:
    """Convert point to dictionary for JSON serialization"""
    return {"x": hex(point.x), "y": hex(point.y)}


def dict_to_point(d: dict) -> Point:
    """Convert dictionary to point"""
    return Point(int(d["x"], 16), int(d["y"], 16))


