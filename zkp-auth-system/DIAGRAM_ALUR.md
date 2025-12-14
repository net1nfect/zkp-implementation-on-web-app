# 📊 Diagram Alur Zero-Knowledge Proof Authentication

## 🔄 Diagram Lengkap: Registrasi → Login

```
┌─────────────────────────────────────────────────────────────────┐
│                    ALUR REGISTRASI                              │
└─────────────────────────────────────────────────────────────────┘

User                    Browser                    Server          Database
 │                         │                         │                │
 │ 1. Input username       │                         │                │
 │────────────────────────>│                         │                │
 │                         │                         │                │
 │                         │ 2. Generate key pair    │                │
 │                         │    privateKey = random()│                │
 │                         │    publicKey = priv*G    │                │
 │                         │                         │                │
 │                         │ 3. Store in localStorage│                │
 │                         │    - zkp_private_key    │                │
 │                         │    - zkp_public_key      │                │
 │                         │    - zkp_username        │                │
 │                         │                         │                │
 │                         │ 4. POST /api/register   │                │
 │                         │    {username, publicKey}│                │
 │                         │────────────────────────>│                │
 │                         │                         │                │
 │                         │                         │ 5. Save to DB  │
 │                         │                         │────────────────>│
 │                         │                         │                │
 │                         │                         │ 6. Return OK  │
 │                         │<────────────────────────│                │
 │                         │                         │                │
 │ 7. Success message      │                         │                │
 │<────────────────────────│                         │                │
 │                         │                         │                │

┌─────────────────────────────────────────────────────────────────┐
│                    ALUR LOGIN                                   │
└─────────────────────────────────────────────────────────────────┘

User                    Browser                    Server          Database
 │                         │                         │                │
 │ 1. Input username       │                         │                │
 │────────────────────────>│                         │                │
 │                         │                         │                │
 │                         │ 2. Get from localStorage│                │
 │                         │    privateKey           │                │
 │                         │    publicKey            │                │
 │                         │                         │                │
 │                         │ 3. Generate ZKP Proof:  │                │
 │                         │    r = random()         │                │
 │                         │    R = r * G            │                │
 │                         │    c = H(R||Y||msg)     │                │
 │                         │    s = r + c*x (mod n)   │                │
 │                         │                         │                │
 │                         │ 4. POST /api/login      │                │
 │                         │    {username, proof}    │                │
 │                         │────────────────────────>│                │
 │                         │                         │                │
 │                         │                         │ 5. Get from DB │
 │                         │                         │<───────────────│
 │                         │                         │  publicKey     │
 │                         │                         │                │
 │                         │                         │ 6. Verify:     │
 │                         │                         │  s*G == R+c*Y  │
 │                         │                         │                │
 │                         │                         │ 7. If valid:   │
 │                         │                         │  Create session│
 │                         │                         │                │
 │                         │ 8. Return result        │                │
 │                         │<────────────────────────│                │
 │                         │                         │                │
 │ 9. Success/Error        │                         │                │
 │<────────────────────────│                         │                │
 │                         │                         │                │
```

## 🔐 Detail ZKP Proof Generation

```
┌─────────────────────────────────────────────────────────────┐
│         PROOF GENERATION (Di Browser)                        │
└─────────────────────────────────────────────────────────────┘

Input:
  - privateKey (x): 0x1cafeea1c14a2a2c8ef610bf6e502aecee6284944cbcb448f06ed32aee5c3721
  - publicKey (Y):  Point(x, y)

Step 1: Generate Random Nonce
  r = random(1, CURVE_N-1)
  → r = 0x5f3a2b1c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f

Step 2: Compute Commitment
  R = r * G  (elliptic curve multiplication)
  → R = Point(0x6c27f3a9..., 0xa5f80dc7...)

Step 3: Generate Challenge
  c = SHA256(R || Y || "authentication") % CURVE_N
  → c = 0x33bf44c629e9c4df635be80dfc08d1fef2f59a7d763049ab61c406acf272cea0

Step 4: Compute Response
  s = (r + c * x) % CURVE_N
  → s = 0x86cea798e5ae7901a64732505c3f0d8efb0a6ff06e3113fa07fc4d4ce86f3d55

Output Proof:
  {
    R: {x: 0x6c27f3a9..., y: 0xa5f80dc7...},
    s: 0x86cea798...,
    c: 0x33bf44c6...
  }
```

## ✅ Detail ZKP Proof Verification

```
┌─────────────────────────────────────────────────────────────┐
│         PROOF VERIFICATION (Di Server)                      │
└─────────────────────────────────────────────────────────────┘

Input:
  - proof: {R, s, c}
  - publicKey (Y): from database

Step 1: Extract Components
  R = dict_to_point(proof["R"])
  s = int(proof["s"], 16)
  c = int(proof["c"], 16)

Step 2: Verify Challenge
  calculated_c = SHA256(R || Y || "authentication") % CURVE_N
  if c != calculated_c:
      return False  # Proof tampered

Step 3: Verify Proof Equation
  left_side = s * G
  right_side = R + c * Y
  
  if left_side == right_side:
      return True   # Proof valid!
  else:
      return False  # Proof invalid

Mathematical Proof:
  s = r + c * x
  s * G = (r + c * x) * G
  s * G = r * G + c * x * G
  s * G = R + c * Y  ✓
```

## 🚨 Skenario: Login dengan Username yang Sama

### **Skenario A: User yang Benar**

```
User A (Pemilik Private Key)
 │
 │ 1. Login dengan username "idhamakbar"
 │
 │ 2. Browser A memiliki private key di localStorage
 │    privateKey = 0x1cafeea1c14a2a2c8ef610bf6e502aecee6284944cbcb448f06ed32aee5c3721
 │
 │ 3. Generate proof dengan private key yang benar
 │    proof = {R, s, c} dimana s = r + c * privateKey
 │
 │ 4. Server verifikasi:
 │    s * G == R + c * Y  ✓
 │
 │ 5. ✅ LOGIN BERHASIL
```

### **Skenario B: User Palsu (Tidak Punya Private Key)**

```
User B (Penyerang)
 │
 │ 1. Login dengan username "idhamakbar" (milik User A)
 │
 │ 2. Browser B TIDAK memiliki private key User A
 │    (atau memiliki private key yang berbeda)
 │
 │ 3. User B mencoba generate proof:
 │    - Jika tidak punya private key: tidak bisa generate proof
 │    - Jika punya private key lain: proof tidak valid
 │
 │ 4. Server verifikasi:
 │    s * G != R + c * Y  ✗
 │
 │ 5. ❌ LOGIN GAGAL
 │
 │ Mengapa gagal?
 │ Karena untuk membuat s yang valid, User B harus:
 │   s = r + c * privateKey_A
 │ Tapi User B tidak tahu privateKey_A!
```

### **Skenario C: User Login dari Browser Lain**

```
User A (Pemilik Private Key)
 │
 │ 1. Register dari Browser A (Chrome di Laptop)
 │    → Private key tersimpan di localStorage Browser A
 │
 │ 2. Login dari Browser B (Firefox di HP)
 │    → Browser B TIDAK memiliki private key
 │
 │ 3. Browser B tidak bisa generate proof
 │
 │ 4. ❌ LOGIN GAGAL
 │
 │ Solusi: Register ulang dari Browser B
 │ (atau implement fitur export/import key)
```

## 🔒 Keamanan: Mengapa Sistem Ini Aman?

```
┌─────────────────────────────────────────────────────────────┐
│                    KEAMANAN SISTEM                            │
└─────────────────────────────────────────────────────────────┘

1. PRIVATE KEY TIDAK PERNAH DIKIRIM
   ┌─────────┐
   │ Browser │ → Proof (R, s, c) → Server
   │         │   ⚠️ Private key tetap di browser
   └─────────┘

2. PROOF TIDAK BISA DIREPLAY
   Setiap login menggunakan random r yang berbeda
   Proof lama tidak bisa digunakan lagi

3. TIDAK BISA MENEBAK PRIVATE KEY
   Private key: 256-bit random number
   Probabilitas menebak: 1 / 2^256 ≈ 0

4. MATHEMATICAL PROOF
   Verifikasi menggunakan elliptic curve cryptography
   Tidak bisa dipalsukan tanpa private key

5. CHALLENGE VERIFICATION
   Server memverifikasi challenge c
   Mencegah proof tampering
```

## 📋 Checklist: Apa yang Disimpan di Mana?

```
┌─────────────────────────────────────────────────────────────┐
│                    LOKASI DATA                               │
└─────────────────────────────────────────────────────────────┘

BROWSER (localStorage):
  ✅ zkp_private_key    → Hanya di browser user
  ✅ zkp_public_key     → Copy dari yang dikirim ke server
  ✅ zkp_username       → Untuk validasi

SERVER (Database):
  ✅ username           → Identifier user
  ✅ public_key_x       → Public key X coordinate
  ✅ public_key_y       → Public key Y coordinate
  ❌ private_key        → TIDAK PERNAH disimpan di server!

NETWORK (Request/Response):
  ✅ public_key         → Hanya saat register
  ✅ proof (R, s, c)    → Hanya saat login
  ❌ private_key        → TIDAK PERNAH dikirim!
```

## 🎯 Kesimpulan Visual

```
REGISTRASI:
User → [Generate Keys] → [Store Private Key Locally]
     → [Send Public Key] → Server → Database

LOGIN:
User → [Get Private Key] → [Generate Proof]
     → [Send Proof] → Server → [Verify Proof]
     → [Create Session] → Success

KEAMANAN:
✅ Private key: Hanya di browser
✅ Proof: Tidak bisa di-replay
✅ Verification: Mathematical proof
✅ Uniqueness: Satu username = satu public key
```

---

**File ini melengkapi `ALUR_DETAIL.md` dengan diagram visual yang lebih jelas!**

