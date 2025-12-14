# Zero-Knowledge Proof Authentication System

Sistem autentikasi berbasis **Zero-Knowledge Proof** menggunakan protokol **Schnorr**. Sistem ini memungkinkan pengguna untuk membuktikan bahwa mereka mengetahui private key tanpa harus mengirimkan private key tersebut ke server.

## 🔐 Konsep Zero-Knowledge Proof

Zero-Knowledge Proof (ZKP) adalah protokol kriptografi yang memungkinkan satu pihak (Prover) membuktikan kepada pihak lain (Verifier) bahwa mereka mengetahui suatu rahasia tanpa mengungkapkan rahasia tersebut.

### Protokol Schnorr

Protokol Schnorr adalah salah satu implementasi ZKP yang efisien:

1. **Prover** menghasilkan random nonce `r` dan menghitung `R = r * G`
2. **Verifier** (atau hash function) menghasilkan challenge `c = H(R || Y || message)`
3. **Prover** menghitung response `s = r + c * x (mod n)`
4. **Verifier** memverifikasi: `s * G == R + c * Y`

Dimana:
- `x` = private key (rahasia)
- `Y` = public key = `x * G`
- `G` = generator point pada elliptic curve
- `r` = random nonce
- `c` = challenge
- `s` = response

## 📐 Arsitektur Sistem

```
┌─────────┐      ┌──────────────┐      ┌───────────┐
│ Client  │ ◄──► │   Frontend   │ ◄──► │  Backend  │
│ (Browser)│      │   (JS/HTML)  │      │ (Python)  │
└─────────┘      └──────────────┘      └─────┬─────┘
                                              │
                                         ┌─────┐
                                         │ DB  │
                                         └─────┘
```

## 🚀 Instalasi dan Setup

### Prerequisites

- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Langkah-langkah Instalasi

1. **Clone atau download project ini**

2. **Masuk ke direktori project**
   ```bash
   cd zkp-auth-system
   ```

3. **Buat virtual environment (opsional tapi direkomendasikan)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Jalankan aplikasi**
   ```bash
   cd backend
   python app.py
   ```

6. **Buka browser dan akses**
   ```
   http://localhost:5000
   ```

## 📁 Struktur Project

```
zkp-auth-system/
│
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Konfigurasi sistem
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── schnorr_auth.py    # Implementasi protokol Schnorr
│   │   ├── crypto_utils.py    # Utility kriptografi (elliptic curve)
│   │   └── session_manager.py # Manajemen session
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py            # Model database untuk user
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py     # Route untuk autentikasi
│   │   └── api_routes.py      # Route API umum
│   ├── static/
│   │   └── js/
│   │       └── zkp-client.js  # Client-side ZKP implementation
│   └── templates/
│       ├── base.html          # Template dasar
│       ├── index.html         # Halaman utama
│       ├── register.html      # Halaman registrasi
│       └── login.html         # Halaman login
│
├── requirements.txt           # Python dependencies
├── .gitignore
└── README.md                  # Dokumentasi ini
```

## 🔄 Alur Authentication

### 1. Registrasi (Registration)

1. User memasukkan username
2. Browser generate key pair (private key `x`, public key `Y = x*G`)
3. Private key disimpan di localStorage browser (tidak pernah dikirim ke server)
4. Public key dikirim ke server dan disimpan di database

### 2. Login (Authentication)

1. User memasukkan username
2. Browser mengambil private key dari localStorage
3. Browser generate ZKP proof:
   - Generate random `r`
   - Hitung `R = r * G`
   - Hitung challenge `c = H(R || Y || "authentication")`
   - Hitung response `s = r + c * x (mod n)`
4. Proof `(R, s, c)` dikirim ke server
5. Server verifikasi proof:
   - Hitung `s * G`
   - Hitung `R + c * Y`
   - Verifikasi apakah `s * G == R + c * Y`
6. Jika valid, server membuat session untuk user

## 🛠️ Teknologi yang Digunakan

- **Backend**: Flask (Python web framework)
- **Database**: SQLite (dapat diganti dengan PostgreSQL/MySQL)
- **Cryptography**: 
  - Elliptic Curve: secp256k1 (sama dengan Bitcoin)
  - Hash Function: SHA-256
  - Protocol: Schnorr ZKP

## 🔒 Keamanan

### Fitur Keamanan

1. **Private Key Tidak Pernah Dikirim**: Private key tetap di browser, tidak pernah dikirim ke server
2. **Zero-Knowledge Proof**: Server hanya memverifikasi proof tanpa mengetahui private key
3. **Session Management**: Session token untuk menjaga state autentikasi
4. **Cryptographically Secure**: Menggunakan elliptic curve cryptography yang sama dengan Bitcoin

### Catatan Penting

⚠️ **Untuk Production**:
- Gunakan HTTPS untuk semua komunikasi
- Simpan private key di secure storage (bukan localStorage)
- Gunakan database production (PostgreSQL/MySQL)
- Set `SESSION_COOKIE_SECURE = True` di config.py
- Generate `SECRET_KEY` yang kuat dan aman
- Implementasikan rate limiting untuk mencegah brute force

## 📝 API Endpoints

### Registration
```
POST /api/register
Body: {
    "username": "user123",
    "public_key": {
        "x": "0x...",
        "y": "0x..."
    }
}
```

### Login
```
POST /api/login
Body: {
    "username": "user123",
    "proof": {
        "R": {"x": "0x...", "y": "0x..."},
        "s": "0x...",
        "c": "0x..."
    }
}
```

### Logout
```
POST /api/logout
```

### Verify Session
```
GET /api/verify-session
```

## 🧪 Testing

Untuk menguji sistem:

1. Buka `http://localhost:5000`
2. Klik "Register" dan buat akun baru
3. Klik "Login" dan autentikasi menggunakan proof
4. Verifikasi bahwa session berhasil dibuat

## 📚 Referensi

- [Schnorr Signature](https://en.wikipedia.org/wiki/Schnorr_signature)
- [Zero-Knowledge Proof](https://en.wikipedia.org/wiki/Zero-knowledge_proof)
- [Elliptic Curve Cryptography](https://en.wikipedia.org/wiki/Elliptic-curve_cryptography)
- [secp256k1](https://en.bitcoin.it/wiki/Secp256k1)

## 👨‍💻 Pengembangan

### Menambahkan Fitur Baru

1. **Password Recovery**: Implementasikan recovery mechanism menggunakan backup key
2. **Multi-factor Authentication**: Tambahkan 2FA untuk keamanan ekstra
3. **Key Rotation**: Implementasikan mekanisme untuk rotate keys
4. **Audit Logging**: Tambahkan logging untuk audit trail

## 📄 License

Project ini dibuat untuk tujuan edukasi dan pembelajaran.

## 🤝 Kontribusi

Silakan buat issue atau pull request jika ingin berkontribusi!

---

**Dibuat dengan ❤️ untuk pembelajaran Zero-Knowledge Proof**

