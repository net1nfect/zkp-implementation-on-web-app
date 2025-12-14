# 🚀 Quick Start Guide

Panduan cepat untuk menjalankan sistem ZKP Authentication.

## ⚡ Instalasi Cepat (5 Menit)

### 1. Install Dependencies

```bash
cd zkp-auth-system
pip install -r requirements.txt
```

### 2. Jalankan Server

```bash
cd backend
python app.py
```

### 3. Buka Browser

Buka: `http://localhost:5000`

## 📝 Langkah-langkah Testing

### Step 1: Register
1. Klik tombol **"Register"**
2. Masukkan username (contoh: `alice`)
3. Klik **"Generate Keys & Register"**
4. ✅ Private key akan disimpan di browser (localStorage)
5. ✅ Public key akan dikirim ke server

### Step 2: Login
1. Klik tombol **"Login"**
2. Masukkan username yang sama (`alice`)
3. Klik **"Generate Proof & Login"**
4. ✅ Browser akan generate ZKP proof
5. ✅ Server akan verifikasi proof
6. ✅ Jika valid, session akan dibuat

### Step 3: Verify
1. Setelah login, Anda akan melihat status **"Authenticated"**
2. Private key Anda **tidak pernah** dikirim ke server
3. Hanya proof yang dikirim

## 🔍 Verifikasi di Browser

Buka **Developer Tools** (F12) → **Application** → **Local Storage**:

Anda akan melihat:
- `zkp_private_key`: Private key Anda (tetap di browser)
- `zkp_public_key`: Public key Anda
- `zkp_username`: Username Anda
- `session_token`: Token session (setelah login)

## ⚠️ Troubleshooting

### Error: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error: "Address already in use"
Port 5000 sudah digunakan. Ubah port di `app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Error: "No keys found"
- Pastikan Anda sudah register terlebih dahulu
- Cek localStorage di browser

## 📚 Dokumentasi Lengkap

- **README.md**: Dokumentasi lengkap sistem
- **TUTORIAL.md**: Tutorial step-by-step dari awal

## 🎯 Next Steps

1. Baca **TUTORIAL.md** untuk memahami konsep ZKP
2. Eksplorasi kode di `backend/auth/` untuk memahami implementasi
3. Coba modifikasi challenge atau tambahkan fitur baru

---

**Selamat mencoba! 🎉**

