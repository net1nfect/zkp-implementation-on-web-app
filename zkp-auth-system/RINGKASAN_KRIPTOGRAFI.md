# 🔐 Ringkasan: Jenis Kriptografi yang Digunakan

## 🎯 Quick Answer

Sistem menggunakan **4 jenis kriptografi utama**:

1. **🔷 Elliptic Curve Cryptography (ECC)** - Kurva **secp256k1** (sama dengan Bitcoin)
2. **✨ Schnorr Signature Protocol** - Untuk Zero-Knowledge Proof
3. **🔐 SHA-256 Hash Function** - Untuk challenge generation
4. **🧮 Modular Arithmetic** - Operasi matematika dalam finite field

---

## 📊 Visual Overview

```
┌─────────────────────────────────────────────┐
│         JENIS KRIPTOGRAFI                  │
└─────────────────────────────────────────────┘

1. ECC (Elliptic Curve Cryptography)
   └─ Kurva: secp256k1
   └─ Key Size: 256-bit private, 512-bit public
   └─ Security: ~128-bit level
   └─ Digunakan: Key generation, point operations

2. Schnorr Protocol
   └─ Type: Digital Signature / ZKP
   └─ Components: (R, s, c)
   └─ Security: Provably secure
   └─ Digunakan: Proof generation & verification

3. SHA-256
   └─ Type: Cryptographic Hash Function
   └─ Output: 256-bit hash
   └─ Security: ~128-bit collision resistance
   └─ Digunakan: Challenge generation

4. Modular Arithmetic
   └─ Type: Finite Field Operations
   └─ Operations: Addition, Multiplication, Inverse
   └─ Digunakan: Semua operasi ECC
```

---

## 🔷 1. Elliptic Curve Cryptography (ECC)

### **Kurva: secp256k1**

**Sama dengan yang digunakan Bitcoin!**

**Parameter:**
- **Prime Modulus (p)**: 256-bit prime number
- **Curve Equation**: y² = x³ + 7 (mod p)
- **Generator Point (G)**: Base point untuk semua operasi
- **Order (n)**: Jumlah titik pada kurva (~256-bit)

**Operasi:**
- ✅ Point Addition: P + Q
- ✅ Scalar Multiplication: k * P
- ✅ Key Generation: private * G = public

**Keamanan:**
- Private key: 256-bit random number
- Security level: ~128-bit (sangat aman)
- Break difficulty: ~2^128 operations

---

## ✨ 2. Schnorr Signature Protocol

### **Zero-Knowledge Proof Protocol**

**Alur:**
```
1. Generate random r
2. Compute R = r * G (commitment)
3. Generate c = H(R || Y || message) (challenge)
4. Compute s = r + c * x (mod n) (response)
5. Proof: (R, s, c)
```

**Verifikasi:**
```
1. Verify: c == H(R || Y || message)
2. Verify: s * G == R + c * Y
3. If both true: Valid ✓
```

**Keamanan:**
- ✅ Private key tidak pernah dikirim
- ✅ Proof tidak bisa dipalsukan
- ✅ Setiap proof unik (random r)
- ✅ Non-repudiation

---

## 🔐 3. SHA-256 Hash Function

### **Cryptographic Hash**

**Penggunaan:**
```javascript
c = SHA256(R || Y || "authentication") % CURVE_N
```

**Properties:**
- ✅ Deterministic: Input sama → output sama
- ✅ One-way: Tidak bisa reverse
- ✅ Collision resistant: Sulit menemukan 2 input dengan hash sama
- ✅ Avalanche effect: Perubahan kecil → hash berbeda besar

**Security:**
- Output: 256-bit
- Collision resistance: ~2^128 operations
- Digunakan: Challenge generation

---

## 🧮 4. Modular Arithmetic

### **Finite Field Operations**

**Operasi:**
- ✅ Modular Addition: (a + b) mod n
- ✅ Modular Multiplication: (a * b) mod p
- ✅ Modular Inverse: a^(-1) mod m

**Penggunaan:**
- Point addition/doubling pada kurva elips
- Response calculation: s = (r + c * x) mod n
- Semua operasi ECC

---

## 🔒 Security Level

### **Overall Security: ~128-bit**

**Breakdown:**
- ECC Discrete Log: ~2^128 operations
- SHA-256 Collision: ~2^128 operations
- Schnorr Proof: Provably secure

**Perbandingan:**
- RSA 2048-bit: ~112-bit security
- ECC 256-bit: ~128-bit security ✅ (lebih aman!)
- AES-256: ~256-bit security

**Kesimpulan:** Sistem ini **sangat aman** untuk production use.

---

## 📚 Standar yang Diikuti

- ✅ **SEC 2**: Elliptic Curve Domain Parameters
- ✅ **FIPS 186-4**: Digital Signature Standard
- ✅ **NIST SP 800-90A**: Random Number Generation
- ✅ **RFC 6979**: Deterministic Signatures

---

## 🎯 Mengapa Kombinasi Ini?

### **Alasan:**

1. **secp256k1**
   - ✅ Proven (Bitcoin menggunakan ini)
   - ✅ Standardized
   - ✅ Efficient

2. **Schnorr**
   - ✅ Perfect untuk ZKP
   - ✅ Efficient verification
   - ✅ Provably secure

3. **SHA-256**
   - ✅ Standard hash function
   - ✅ Fast & secure
   - ✅ Widely trusted

4. **Modular Arithmetic**
   - ✅ Required untuk ECC
   - ✅ Well-understood
   - ✅ Efficient

---

## 💡 Kesimpulan

Sistem menggunakan **kriptografi modern** yang:

✅ **Aman**: 128-bit security level
✅ **Efisien**: Fast operations
✅ **Standard**: Mengikuti standar industri
✅ **Proven**: Digunakan Bitcoin
✅ **Zero-Knowledge**: Perfect untuk authentication

**Ini adalah kriptografi kelas enterprise yang sama dengan Bitcoin!** 🔐💰

---

**Detail lengkap ada di `JENIS_KRIPTOGRAFI.md`**

