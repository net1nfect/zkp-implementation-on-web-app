# 🔐 Jenis Kriptografi yang Digunakan

## 📋 Ringkasan

Sistem ZKP Authentication menggunakan kombinasi beberapa jenis kriptografi modern:

1. **Elliptic Curve Cryptography (ECC)** - secp256k1
2. **Schnorr Signature Protocol** - Zero-Knowledge Proof
3. **SHA-256 Hash Function** - Cryptographic hashing
4. **Modular Arithmetic** - Finite field operations

---

## 1. 🔷 Elliptic Curve Cryptography (ECC)

### **Apa itu ECC?**

Elliptic Curve Cryptography adalah sistem kriptografi yang menggunakan **matematika kurva elips** untuk keamanan. ECC memberikan tingkat keamanan yang sama dengan RSA tetapi dengan **key size yang lebih kecil**.

### **Kurva yang Digunakan: secp256k1**

Sistem ini menggunakan kurva **secp256k1**, yang sama dengan yang digunakan oleh **Bitcoin**.

**Parameter Kurva:**
```
Prime Modulus (p):
0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

Curve Equation: y² = x³ + 7 (mod p)

Generator Point (G):
x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

Order (n):
0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
```

### **Operasi ECC yang Digunakan:**

#### **a. Point Addition (P + Q)**
Menambahkan dua titik pada kurva elips:
```python
def point_add(p1, p2):
    # Jika p1 == p2: Point Doubling
    # Jika p1 != p2: Point Addition
    # Hasil: Titik baru pada kurva
```

#### **b. Scalar Multiplication (k * P)**
Mengalikan titik dengan skalar:
```python
def point_multiply(k, point):
    # k * point = point + point + ... + point (k kali)
    # Menggunakan binary method untuk efisiensi
```

#### **c. Key Generation**
```python
private_key = random(1, n-1)  # Random 256-bit number
public_key = private_key * G  # Scalar multiplication
```

**Keamanan:**
- Private key: 256-bit (sangat aman)
- Public key: 512-bit (2 koordinat x, y)
- Computational security: ~2^128 operations untuk break

---

## 2. ✨ Schnorr Signature Protocol

### **Apa itu Schnorr Protocol?**

Schnorr adalah protokol **digital signature** yang efisien dan aman. Dalam konteks ini, digunakan untuk **Zero-Knowledge Proof**.

### **Komponen Schnorr:**

#### **a. Setup**
```
Private Key: x (secret, 256-bit)
Public Key: Y = x * G (public, point pada kurva)
```

#### **b. Proof Generation (Prover)**
```
1. Generate random nonce: r = random(1, n-1)
2. Compute commitment: R = r * G
3. Generate challenge: c = H(R || Y || message)
4. Compute response: s = r + c * x (mod n)
5. Send proof: (R, s, c)
```

#### **c. Proof Verification (Verifier)**
```
1. Receive proof: (R, s, c)
2. Recalculate challenge: c' = H(R || Y || message)
3. Verify: c == c'
4. Verify equation: s * G == R + c * Y
5. If both true: Proof valid ✓
```

### **Mengapa Schnorr?**

✅ **Efisiensi**: Lebih cepat dari ECDSA
✅ **Security**: Provably secure
✅ **Non-malleability**: Tidak bisa dimodifikasi
✅ **Batch verification**: Bisa verifikasi banyak sekaligus
✅ **Zero-Knowledge**: Perfect untuk ZKP

---

## 3. 🔐 SHA-256 Hash Function

### **Apa itu SHA-256?**

SHA-256 (Secure Hash Algorithm 256-bit) adalah fungsi hash kriptografi yang menghasilkan **256-bit hash value**.

### **Penggunaan dalam Sistem:**

#### **a. Challenge Generation**
```javascript
c = SHA256(R || Y || "authentication") % CURVE_N
```

**Input:**
- R: Commitment point (64 bytes)
- Y: Public key point (64 bytes)
- "authentication": Message string

**Output:**
- c: Challenge value (256-bit, modulo n)

#### **b. Properties SHA-256:**

✅ **Deterministic**: Input sama → output sama
✅ **One-way**: Tidak bisa reverse
✅ **Avalanche effect**: Perubahan kecil → hash berbeda besar
✅ **Collision resistant**: Sangat sulit menemukan 2 input dengan hash sama

**Security Level:**
- 256-bit output
- ~2^256 possible outputs
- Computational security: ~2^128 untuk collision

---

## 4. 🧮 Modular Arithmetic

### **Apa itu Modular Arithmetic?**

Operasi matematika dalam **finite field** (modulo prime).

### **Operasi yang Digunakan:**

#### **a. Modular Inverse**
```python
def mod_inverse(a, m):
    # Menghitung a^(-1) mod m
    # Menggunakan Extended Euclidean Algorithm
    return pow(a, -1, m)  # Python 3.8+
```

**Penggunaan:**
- Point addition/doubling
- Slope calculation pada kurva elips

#### **b. Modular Multiplication**
```python
(a * b) % p
```

#### **c. Modular Addition**
```python
(a + b) % n
```

**Penggunaan:**
- Response calculation: `s = (r + c * x) % n`

---

## 5. 📊 Kombinasi Kriptografi

### **Alur Lengkap:**

```
┌─────────────────────────────────────────┐
│ 1. ECC Key Generation                  │
│    → Private key: random(256-bit)      │
│    → Public key: private * G           │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 2. Schnorr Proof Generation             │
│    → Random nonce: r                   │
│    → Commitment: R = r * G (ECC)       │
│    → Challenge: c = SHA256(...)         │
│    → Response: s = r + c*x (mod n)     │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 3. Schnorr Proof Verification          │
│    → Verify challenge: c == SHA256(...) │
│    → Verify equation: s*G == R + c*Y   │
│    → (Menggunakan ECC operations)      │
└─────────────────────────────────────────┘
```

---

## 6. 🔒 Security Properties

### **Keamanan yang Diberikan:**

#### **a. Discrete Logarithm Problem (DLP)**
- **Masalah**: Diberikan Y = x * G, cari x
- **Kesulitan**: Exponential (2^128 operations)
- **Keamanan**: Sangat aman dengan key 256-bit

#### **b. Zero-Knowledge Property**
- **Private key tidak pernah dikirim**
- **Hanya proof yang dikirim**
- **Server tidak bisa mendapatkan private key dari proof**

#### **c. Non-repudiation**
- **Proof tidak bisa dipalsukan** tanpa private key
- **Setiap proof unik** (karena random r)
- **Tidak bisa di-replay** (proof berbeda setiap kali)

#### **d. Forward Secrecy**
- **Setiap login menggunakan random r baru**
- **Proof lama tidak bisa digunakan lagi**
- **Compromise satu proof tidak compromise lainnya**

---

## 7. 📈 Perbandingan dengan Sistem Lain

### **ECC vs RSA:**

| Aspek | ECC (256-bit) | RSA (2048-bit) |
|-------|---------------|----------------|
| Key Size | 256-bit | 2048-bit |
| Security Level | ~128-bit | ~112-bit |
| Speed | Lebih cepat | Lebih lambat |
| Bandwidth | Lebih kecil | Lebih besar |

**Kesimpulan:** ECC lebih efisien dengan security yang sama atau lebih baik.

### **Schnorr vs ECDSA:**

| Aspek | Schnorr | ECDSA |
|-------|---------|-------|
| Signature Size | 64 bytes | 64 bytes |
| Verification | Lebih cepat | Lebih lambat |
| Batch Verify | Ya | Tidak |
| Zero-Knowledge | Perfect | Tidak ideal |

**Kesimpulan:** Schnorr lebih cocok untuk ZKP.

---

## 8. 🎯 Mengapa Kombinasi Ini?

### **Alasan Pemilihan:**

1. **secp256k1**
   - ✅ Proven security (digunakan Bitcoin)
   - ✅ Standardized
   - ✅ Efficient implementation
   - ✅ 256-bit security level

2. **Schnorr Protocol**
   - ✅ Perfect untuk Zero-Knowledge Proof
   - ✅ Efficient verification
   - ✅ Provably secure
   - ✅ Non-malleable

3. **SHA-256**
   - ✅ Standard hash function
   - ✅ Widely used dan trusted
   - ✅ Fast implementation
   - ✅ 256-bit security

4. **Modular Arithmetic**
   - ✅ Required untuk ECC
   - ✅ Efficient dengan Python/JavaScript
   - ✅ Well-understood mathematics

---

## 9. 📚 Referensi & Standar

### **Standar yang Diikuti:**

- **SEC 2**: Recommended Elliptic Curve Domain Parameters
- **FIPS 186-4**: Digital Signature Standard
- **NIST SP 800-90A**: Random Number Generation
- **RFC 6979**: Deterministic DSA/ECDSA

### **Kurva secp256k1:**

- **Standar**: SEC 2, Recommended Elliptic Curve Domain Parameters
- **Digunakan oleh**: Bitcoin, Ethereum, dan banyak cryptocurrency
- **Security**: 128-bit security level
- **Status**: Well-tested dan trusted

---

## 10. 🔬 Implementasi Detail

### **File-file Kriptografi:**

1. **`crypto_utils.py`**
   - Elliptic curve operations
   - Point addition/multiplication
   - Key generation
   - Hash functions

2. **`schnorr_auth.py`**
   - Schnorr protocol implementation
   - Proof generation
   - Proof verification

3. **`zkp-client.js`**
   - Client-side ECC operations
   - Proof generation di browser
   - JavaScript BigInt untuk precision

### **Library yang Digunakan:**

- **Python**: Built-in `pow()` untuk modular inverse
- **JavaScript**: Web Crypto API untuk random, SHA-256
- **No external crypto libraries**: Pure implementation

---

## 📊 Kesimpulan

Sistem menggunakan **kombinasi kriptografi modern** yang:

✅ **Aman**: 256-bit security level
✅ **Efisien**: Fast operations
✅ **Standard**: Mengikuti standar industri
✅ **Proven**: Digunakan oleh Bitcoin dan sistem kripto lainnya
✅ **Zero-Knowledge**: Perfect untuk authentication tanpa reveal secret

**Overall Security Level: ~128-bit** (sangat aman untuk production)

---

**Ini adalah kombinasi kriptografi yang sama dengan yang digunakan Bitcoin!** 🔐💰

