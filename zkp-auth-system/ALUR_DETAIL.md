# 📚 Penjelasan Detail Alur Zero-Knowledge Proof Authentication

## 🎯 Konsep Dasar

Zero-Knowledge Proof (ZKP) memungkinkan seseorang membuktikan bahwa mereka mengetahui suatu rahasia (private key) **tanpa mengungkapkan rahasia tersebut**.

---

## 📝 ALUR 1: REGISTRASI (Registration)

### **Step-by-Step Detail:**

#### **1. User Mengakses Halaman Register**
```
User → Browser → http://localhost:5000/register
```

#### **2. User Memasukkan Username**
- User memasukkan username (contoh: `idhamakbar`)
- Username ini akan menjadi identifier di database

#### **3. Browser Generate Key Pair** 🔑
**Di Browser (JavaScript - `zkp-client.js`):**

```javascript
// Generate private key (random 256-bit number)
privateKey = random_number_between(1, CURVE_N-1)
// Contoh: 0x1cafeea1c14a2a2c8ef610bf6e502aecee6284944cbcb448f06ed32aee5c3721

// Generate public key = privateKey * G (elliptic curve multiplication)
publicKey = privateKey * G
// Contoh: 
//   x = 0xab7c7ce71f1820e45e83faab973746b2c420f708be5b2c1825d8ec1a6512c86c
//   y = 0x4c91d1c87d211a3558d023c0180655e32d51e80e530bab07e54dae75ab000dbd
```

**PENTING:**
- Private key **TIDAK PERNAH** dikirim ke server
- Private key disimpan di **localStorage browser** (hanya di device user)
- Hanya public key yang dikirim ke server

#### **4. Browser Menyimpan Key di LocalStorage**
```javascript
localStorage.setItem('zkp_private_key', privateKey.toString())
localStorage.setItem('zkp_public_key', JSON.stringify({
    x: '0x...',
    y: '0x...'
}))
localStorage.setItem('zkp_username', 'idhamakbar')
```

**Lokasi Penyimpanan:**
- Private key: **Hanya di browser user** (localStorage)
- Public key: **Di browser** (localStorage) **DAN di server** (database)

#### **5. Browser Mengirim Public Key ke Server**
**Request ke Server:**
```json
POST /api/register
{
    "username": "idhamakbar",
    "public_key": {
        "x": "0xab7c7ce71f1820e45e83faab973746b2c420f708be5b2c1825d8ec1a6512c86c",
        "y": "0x4c91d1c87d211a3558d023c0180655e32d51e80e530bab07e54dae75ab000dbd"
    }
}
```

#### **6. Server Menyimpan di Database**
**Di Server (Python - `auth_routes.py`):**

```python
# Server menerima public key
# Menyimpan ke database SQLite
User(
    username="idhamakbar",
    public_key_x="0xab7c7ce71f1820e45e83faab973746b2c420f708be5b2c1825d8ec1a6512c86c",
    public_key_y="0x4c91d1c87d211a3558d023c0180655e32d51e80e530bab07e54dae75ab000dbd"
)
```

**Database Structure:**
```
Table: users
- id: 1
- username: "idhamakbar"
- public_key_x: "0xab7c7ce71f1820e45e83faab973746b2c420f708be5b2c1825d8ec1a6512c86c"
- public_key_y: "0x4c91d1c87d211a3558d023c0180655e32d51e80e530bab07e54dae75ab000dbd"
- created_at: "2024-01-01 12:00:00"
```

#### **7. Server Mengirim Response Sukses**
```json
{
    "message": "Registration successful",
    "user_id": 1,
    "username": "idhamakbar"
}
```

### **📊 Diagram Alur Registrasi:**

```
┌─────────┐
│  User   │
└────┬────┘
     │ 1. Input username: "idhamakbar"
     ▼
┌─────────────────┐
│    Browser      │
│  (JavaScript)   │
└────┬────────────┘
     │ 2. Generate key pair
     │    privateKey = random()
     │    publicKey = privateKey * G
     │
     │ 3. Store in localStorage:
     │    - zkp_private_key
     │    - zkp_public_key
     │    - zkp_username
     │
     │ 4. Send to server:
     │    POST /api/register
     │    {username, public_key}
     ▼
┌─────────────────┐
│     Server      │
│    (Python)     │
└────┬────────────┘
     │ 5. Save to database
     │    - username
     │    - public_key_x
     │    - public_key_y
     │
     │ 6. Return success
     ▼
┌─────────┐
│  User   │
│ Success │
└─────────┘
```

---

## 🔐 ALUR 2: LOGIN (Authentication dengan ZKP)

### **Step-by-Step Detail:**

#### **1. User Mengakses Halaman Login**
```
User → Browser → http://localhost:5000/login
```

#### **2. User Memasukkan Username**
- User memasukkan username: `idhamakbar`
- Browser memvalidasi bahwa username di localStorage sama

#### **3. Browser Mengambil Private Key dari LocalStorage**
**Di Browser:**
```javascript
privateKey = BigInt(localStorage.getItem('zkp_private_key'))
// Contoh: 0x1cafeea1c14a2a2c8ef610bf6e502aecee6284944cbcb448f06ed32aee5c3721

publicKey = {
    x: BigInt(JSON.parse(localStorage.getItem('zkp_public_key')).x),
    y: BigInt(JSON.parse(localStorage.getItem('zkp_public_key')).y)
}
```

**PENTING:** Private key **TIDAK PERNAH** dikirim ke server!

#### **4. Browser Generate ZKP Proof** 🎯

**Ini adalah inti dari Zero-Knowledge Proof!**

**Step 4a: Generate Random Nonce `r`**
```javascript
r = random_number_between(1, CURVE_N-1)
// Contoh: 0x5f3a2b1c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f
```

**Step 4b: Compute Commitment `R = r * G`**
```javascript
R = r * G  // Elliptic curve multiplication
// R adalah "commitment" - komitmen tanpa mengungkapkan r
// Contoh:
//   R.x = 0x6c27f3a9e49567403f7440d7b28efde67882f76dd1bf123d29ee79ce07cdc259
//   R.y = 0xa5f80dc78a1a14e1c504a3458029f3dfdf8e213e9b49a78142d26a86f6e14698
```

**Step 4c: Generate Challenge `c = H(R || Y || message)`**
```javascript
// Hash function: SHA-256
c = SHA256(R || publicKey || "authentication") % CURVE_N
// Contoh: 0x33bf44c629e9c4df635be80dfc08d1fef2f59a7d763049ab61c406acf272cea0
```

**Step 4d: Compute Response `s = r + c * privateKey (mod n)`**
```javascript
s = (r + c * privateKey) % CURVE_N
// Contoh: 0x86cea798e5ae7901a64732505c3f0d8efb0a6ff06e3113fa07fc4d4ce86f3d55
```

**Proof yang dihasilkan:**
```json
{
    "R": {
        "x": "0x6c27f3a9e49567403f7440d7b28efde67882f76dd1bf123d29ee79ce07cdc259",
        "y": "0xa5f80dc78a1a14e1c504a3458029f3dfdf8e213e9b49a78142d26a86f6e14698"
    },
    "s": "0x86cea798e5ae7901a64732505c3f0d8efb0a6ff06e3113fa07fc4d4ce86f3d55",
    "c": "0x33bf44c629e9c4df635be80dfc08d1fef2f59a7d763049ab61c406acf272cea0"
}
```

#### **5. Browser Mengirim Proof ke Server**
**Request:**
```json
POST /api/login
{
    "username": "idhamakbar",
    "proof": {
        "R": {"x": "0x...", "y": "0x..."},
        "s": "0x...",
        "c": "0x..."
    }
}
```

**PENTING:** 
- Private key **TIDAK** dikirim
- Hanya proof (R, s, c) yang dikirim
- Proof ini **tidak bisa digunakan untuk login ulang** (karena menggunakan random `r`)

#### **6. Server Memverifikasi Proof** ✅

**Di Server (`schnorr_auth.py`):**

**Step 6a: Ambil Public Key dari Database**
```python
user = database.get_user("idhamakbar")
publicKey = Point(
    int(user.public_key_x, 16),
    int(user.public_key_y, 16)
)
```

**Step 6b: Verifikasi Challenge**
```python
# Recalculate challenge
calculated_c = SHA256(R || publicKey || "authentication") % CURVE_N

# Verify challenge matches
if c != calculated_c:
    return False  # Proof invalid or tampered
```

**Step 6c: Verifikasi Proof (Inti Verifikasi)**
```python
# Verify: s * G == R + c * Y

# Left side: s * G
left_side = s * G

# Right side: R + c * Y
cY = c * publicKey  # c * Y
right_side = R + cY  # R + c * Y

# Check equality
if left_side == right_side:
    return True  # Proof valid!
else:
    return False  # Proof invalid
```

**Mengapa ini bekerja?**

Karena:
- `s = r + c * privateKey`
- `s * G = (r + c * privateKey) * G`
- `s * G = r * G + c * privateKey * G`
- `s * G = R + c * Y` ✓

Jadi jika proof valid, berarti user **memiliki private key** yang sesuai dengan public key di database!

#### **7. Server Membuat Session**
```python
if proof_valid:
    session_token = create_session(user_id, username)
    return {
        "message": "Login successful",
        "session_token": "...",
        "user": {...}
    }
```

### **📊 Diagram Alur Login:**

```
┌─────────┐
│  User   │
└────┬────┘
     │ 1. Input username: "idhamakbar"
     ▼
┌─────────────────┐
│    Browser      │
│  (JavaScript)   │
└────┬────────────┘
     │ 2. Get private key from localStorage
     │
     │ 3. Generate ZKP Proof:
     │    r = random()
     │    R = r * G
     │    c = H(R || Y || "authentication")
     │    s = r + c * x (mod n)
     │
     │ 4. Send proof (R, s, c) to server
     │    ⚠️ Private key TIDAK dikirim!
     ▼
┌─────────────────┐
│     Server      │
│    (Python)     │
└────┬────────────┘
     │ 5. Get public key from database
     │
     │ 6. Verify proof:
     │    - Verify challenge c
     │    - Verify: s*G == R + c*Y
     │
     │ 7. If valid: Create session
     │    If invalid: Return error
     ▼
┌─────────┐
│ Success │
│ or Error│
└─────────┘
```

---

## 🔒 SKENARIO: Seseorang Login dengan Username yang Sama

### **Skenario 1: User yang Benar (Pemilik Private Key)**

**Situasi:**
- User A register dengan username `idhamakbar`
- User A memiliki private key di browser A
- User A login dari browser A

**Alur:**
1. Browser A mengambil private key dari localStorage
2. Generate proof menggunakan private key yang benar
3. Server verifikasi: `s * G == R + c * Y` ✓
4. **Login berhasil!** ✅

---

### **Skenario 2: User Palsu (Tidak Memiliki Private Key)**

**Situasi:**
- User A register dengan username `idhamakbar`
- User B (penyerang) mencoba login dengan username `idhamakbar`
- User B **TIDAK memiliki private key** User A

**Alur:**
1. User B input username `idhamakbar`
2. Browser B tidak memiliki private key di localStorage
   - Atau memiliki private key yang berbeda
3. Jika User B mencoba generate proof:
   - User B tidak tahu private key User A
   - User B tidak bisa generate proof yang valid
4. Server verifikasi: `s * G != R + c * Y` ✗
5. **Login gagal!** ❌

**Mengapa gagal?**

Karena untuk generate proof yang valid, User B harus:
- Mengetahui private key `x` yang sesuai dengan public key `Y` di database
- Tanpa private key, User B tidak bisa membuat `s = r + c * x` yang valid
- Server akan mendeteksi bahwa `s * G != R + c * Y`

---

### **Skenario 3: User Login dari Device/Browser Lain**

**Situasi:**
- User A register dari Browser A (Chrome di Laptop)
- User A ingin login dari Browser B (Firefox di HP)

**Alur:**
1. Browser B tidak memiliki private key (karena localStorage berbeda per browser)
2. User A tidak bisa login dari Browser B
3. **Login gagal!** ❌

**Solusi:**
- User A harus **register ulang** dari Browser B
- Atau **export/import private key** (fitur ini belum diimplementasikan)

**Ini adalah fitur keamanan!** Private key hanya ada di device yang digunakan untuk register.

---

### **Skenario 4: Multiple User dengan Username Sama (Tidak Mungkin)**

**Situasi:**
- User A register dengan username `idhamakbar`
- User B mencoba register dengan username `idhamakbar` yang sama

**Alur:**
1. User B mencoba register dengan username `idhamakbar`
2. Server cek database: username sudah ada
3. Server return error: "Username already exists"
4. **Registrasi gagal!** ❌

**Mengapa?**

Karena username adalah **unique identifier**. Setiap username hanya bisa memiliki satu public key di database.

---

## 🛡️ Keamanan Sistem

### **1. Private Key Tidak Pernah Dikirim**
- Private key hanya ada di browser user
- Tidak pernah dikirim melalui network
- Tidak ada di database server

### **2. Proof Tidak Bisa Direplay**
- Setiap proof menggunakan random `r` yang berbeda
- Proof yang sudah digunakan tidak bisa digunakan lagi
- Setiap login memerlukan proof baru

### **3. Tidak Bisa Menebak Private Key**
- Private key adalah random 256-bit number
- Probabilitas menebak: 1 / 2^256 (sangat kecil)
- Tidak ada cara untuk mendapatkan private key dari public key

### **4. Challenge Verification**
- Server memverifikasi bahwa challenge `c` sesuai
- Mencegah proof tampering
- Mencegah replay attack

### **5. Mathematical Proof**
- Verifikasi menggunakan matematika elliptic curve
- Tidak bisa dipalsukan tanpa private key
- Cryptographically secure

---

## 📊 Perbandingan: Traditional vs ZKP Authentication

### **Traditional (Password-based):**
```
User → Password → Server
Server: Verify password hash
❌ Password bisa dicuri
❌ Password bisa di-replay
❌ Server tahu password (hash)
```

### **ZKP (Zero-Knowledge Proof):**
```
User → Proof (R, s, c) → Server
Server: Verify s*G == R + c*Y
✅ Private key tidak pernah dikirim
✅ Proof tidak bisa di-replay
✅ Server tidak tahu private key
```

---

## 🎯 Kesimpulan

1. **Registrasi**: User generate key pair, simpan private key lokal, kirim public key ke server
2. **Login**: User generate proof menggunakan private key, server verifikasi tanpa mengetahui private key
3. **Keamanan**: Hanya pemilik private key yang bisa login
4. **Uniqueness**: Setiap username hanya bisa memiliki satu public key
5. **Device-specific**: Private key hanya ada di device yang digunakan untuk register

**Ini adalah keajaiban Zero-Knowledge Proof!** ✨

