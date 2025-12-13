# 🚀 Cara Menjalankan Sistem ZKP Authentication

## 📋 Prerequisites (Yang Diperlukan)

1. **Python 3.8 atau lebih tinggi**
   - Cek versi: `python --version` atau `python3 --version`

2. **pip** (Python package manager)
   - Biasanya sudah terinstall bersama Python

## 🔧 Langkah-langkah Instalasi dan Menjalankan

### **Langkah 1: Buka Terminal/Command Prompt**

- **Windows**: Tekan `Win + R`, ketik `cmd` atau `powershell`, tekan Enter
- **Linux/Mac**: Buka Terminal

### **Langkah 2: Masuk ke Direktori Project**

```bash
cd "d:\kuliah materi\CRYPTO\zkp-auth-system"
```

**Catatan**: Sesuaikan path sesuai lokasi folder Anda.

### **Langkah 3: Buat Virtual Environment (Opsional tapi Direkomendasikan)**

Ini akan mengisolasi dependencies project Anda:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

Setelah diaktifkan, Anda akan melihat `(venv)` di awal command prompt.

### **Langkah 4: Install Dependencies**

```bash
pip install -r requirements.txt
```

Ini akan menginstall:
- Flask (web framework)
- SQLAlchemy (database ORM)
- Werkzeug (WSGI utilities)

**Output yang diharapkan:**
```
Successfully installed Flask-3.0.0 SQLAlchemy-2.0.23 Werkzeug-3.0.1
```

### **Langkah 5: Masuk ke Folder Backend**

```bash
cd backend
```

### **Langkah 6: Jalankan Server**

```bash
python app.py
```

**Output yang diharapkan:**
```
============================================================
ZKP Authentication System - Schnorr Protocol
============================================================
Server starting on http://localhost:5000
============================================================
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### **Langkah 7: Buka Browser**

Buka browser Anda (Chrome, Firefox, Edge, dll) dan akses:

```
http://localhost:5000
```

atau

```
http://127.0.0.1:5000
```

## ✅ Testing Sistem

### **Test 1: Register User Baru**

1. Di browser, klik tombol **"Register"**
2. Masukkan username (contoh: `alice` atau `bob`)
3. Klik **"Generate Keys & Register"**
4. Jika berhasil, akan muncul pesan: **"Registration successful! Your keys have been saved locally."**
5. Anda akan diarahkan ke halaman login

### **Test 2: Login dengan ZKP**

1. Di halaman login, masukkan username yang sama (contoh: `alice`)
2. Klik **"Generate Proof & Login"**
3. Browser akan:
   - Mengambil private key dari localStorage
   - Generate ZKP proof
   - Mengirim proof ke server
4. Jika berhasil, akan muncul pesan: **"Login successful!"**
5. Anda akan diarahkan ke halaman utama dengan status **"Authenticated"**

### **Test 3: Verifikasi di Browser**

1. Tekan **F12** untuk membuka Developer Tools
2. Pilih tab **Application** (Chrome) atau **Storage** (Firefox)
3. Klik **Local Storage** → `http://localhost:5000`
4. Anda akan melihat:
   - `zkp_private_key`: Private key Anda (tetap di browser, tidak pernah dikirim ke server)
   - `zkp_public_key`: Public key Anda
   - `zkp_username`: Username Anda
   - `session_token`: Token session (setelah login)

## 🛑 Menghentikan Server

Untuk menghentikan server, tekan:
- **Ctrl + C** di terminal/command prompt

## ⚠️ Troubleshooting (Mengatasi Masalah)

### **Problem 1: "python: command not found"**

**Solusi:**
- Gunakan `python3` instead of `python`
- Atau install Python dari python.org

### **Problem 2: "pip: command not found"**

**Solusi:**
- Gunakan `python -m pip` atau `python3 -m pip`
- Atau install pip terlebih dahulu

### **Problem 3: "No module named 'flask'"**

**Solusi:**
```bash
pip install Flask SQLAlchemy Werkzeug
```

Atau pastikan virtual environment sudah diaktifkan:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### **Problem 4: "Address already in use" atau "Port 5000 already in use"**

**Solusi 1**: Tutup aplikasi lain yang menggunakan port 5000

**Solusi 2**: Ubah port di `backend/app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Ubah ke port 5001
```

Lalu akses: `http://localhost:5001`

### **Problem 5: "ModuleNotFoundError: No module named 'config'"**

**Solusi**: Pastikan Anda menjalankan dari folder `backend`:
```bash
cd backend
python app.py
```

### **Problem 6: Database Error**

**Solusi**: Database SQLite akan dibuat otomatis saat pertama kali menjalankan. Pastikan folder `backend` memiliki permission write.

### **Problem 7: "No keys found" saat login**

**Solusi**: 
- Pastikan Anda sudah register terlebih dahulu
- Jangan hapus localStorage di browser
- Cek di Developer Tools → Application → Local Storage

### **Problem 8: Import Error di Python**

Jika ada error seperti:
```
ImportError: attempted relative import with no known parent package
```

**Solusi**: Pastikan struktur folder sudah benar dan jalankan dari folder `backend`.

## 📝 Catatan Penting

1. **Private Key**: Private key disimpan di localStorage browser. Jika Anda clear browser data, private key akan hilang dan Anda tidak bisa login lagi.

2. **Database**: Database SQLite (`zkp_auth.db`) akan dibuat otomatis di folder `backend` saat pertama kali register.

3. **Development Mode**: Server berjalan dalam mode development. Untuk production, gunakan server production seperti Gunicorn atau uWSGI.

4. **HTTPS**: Untuk production, wajib menggunakan HTTPS untuk keamanan.

## 🎯 Quick Commands Summary

```bash
# 1. Masuk ke folder project
cd "d:\kuliah materi\CRYPTO\zkp-auth-system"

# 2. (Opsional) Aktifkan virtual environment
venv\Scripts\activate  # Windows
# atau
source venv/bin/activate  # Linux/Mac

# 3. Install dependencies (hanya pertama kali)
pip install -r requirements.txt

# 4. Masuk ke folder backend
cd backend

# 5. Jalankan server
python app.py

# 6. Buka browser: http://localhost:5000
```

## 🎉 Selamat!

Jika semua langkah berhasil, Anda sekarang memiliki sistem autentikasi Zero-Knowledge Proof yang berjalan!

Untuk memahami lebih dalam, baca:
- **README.md**: Dokumentasi lengkap
- **TUTORIAL.md**: Tutorial step-by-step dengan penjelasan konsep

---

**Need Help?** Jika masih ada masalah, pastikan:
1. Python versi 3.8+
2. Semua dependencies terinstall
3. Menjalankan dari folder `backend`
4. Port 5000 tidak digunakan aplikasi lain

