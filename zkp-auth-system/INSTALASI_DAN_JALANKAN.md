# 📖 Panduan Instalasi dan Menjalankan - Bahasa Indonesia

## 🎯 Cara Termudah (Windows)

### **Opsi 1: Menggunakan Script Otomatis** ⭐ (Paling Mudah)

1. **Double-click** file `run.bat` di folder `zkp-auth-system`
2. Script akan otomatis:
   - Membuat virtual environment (jika belum ada)
   - Install dependencies
   - Menjalankan server
3. Buka browser: `http://localhost:5000`

**Selesai!** 🎉

---

## 🔧 Cara Manual (Step by Step)

### **Langkah 1: Buka Command Prompt**

- Tekan `Win + R`
- Ketik `cmd`
- Tekan Enter

### **Langkah 2: Masuk ke Folder Project**

```cmd
cd "d:\kuliah materi\CRYPTO\zkp-auth-system"
```

### **Langkah 3: Buat Virtual Environment** (Opsional)

```cmd
python -m venv venv
venv\Scripts\activate
```

Anda akan melihat `(venv)` di awal command prompt.

### **Langkah 4: Install Dependencies**

```cmd
pip install -r requirements.txt
```

Tunggu sampai selesai. Output yang diharapkan:
```
Successfully installed Flask-3.0.0 SQLAlchemy-2.0.23 Werkzeug-3.0.1
```

### **Langkah 5: Masuk ke Folder Backend**

```cmd
cd backend
```

### **Langkah 6: Jalankan Server**

```cmd
python app.py
```

Anda akan melihat:
```
============================================================
ZKP Authentication System - Schnorr Protocol
============================================================
Server starting on http://localhost:5000
============================================================
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### **Langkah 7: Buka Browser**

Buka browser dan ketik di address bar:
```
http://localhost:5000
```

---

## ✅ Testing Sistem

### **Test 1: Register**

1. Di browser, klik tombol **"Register"**
2. Masukkan username (contoh: `alice`)
3. Klik **"Generate Keys & Register"**
4. Jika berhasil, akan muncul pesan sukses
5. Anda akan diarahkan ke halaman login

### **Test 2: Login**

1. Masukkan username yang sama (`alice`)
2. Klik **"Generate Proof & Login"**
3. Jika berhasil, akan muncul pesan **"Login successful!"**
4. Anda akan melihat status **"Authenticated"** di halaman utama

### **Test 3: Cek Private Key di Browser**

1. Tekan **F12** (Developer Tools)
2. Pilih tab **Application** (Chrome) atau **Storage** (Firefox)
3. Klik **Local Storage** → `http://localhost:5000`
4. Anda akan melihat:
   - `zkp_private_key`: Private key Anda (TIDAK pernah dikirim ke server!)
   - `zkp_public_key`: Public key Anda
   - `zkp_username`: Username Anda

---

## 🛑 Menghentikan Server

Di Command Prompt, tekan:
```
CTRL + C
```

---

## ⚠️ Troubleshooting

### **Masalah: "python: command not found"**

**Solusi:**
- Coba gunakan `py` instead of `python`:
  ```cmd
  py app.py
  ```
- Atau install Python dari [python.org](https://www.python.org/downloads/)

### **Masalah: "pip: command not found"**

**Solusi:**
```cmd
python -m pip install -r requirements.txt
```

### **Masalah: "No module named 'flask'"**

**Solusi:**
```cmd
pip install Flask SQLAlchemy Werkzeug
```

Atau pastikan virtual environment aktif:
```cmd
venv\Scripts\activate
```

### **Masalah: "Address already in use" (Port 5000 sudah digunakan)**

**Solusi 1**: Tutup aplikasi lain yang menggunakan port 5000

**Solusi 2**: Ubah port di `backend/app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```
Lalu akses: `http://localhost:5001`

### **Masalah: "ModuleNotFoundError"**

**Solusi**: Pastikan Anda menjalankan dari folder `backend`:
```cmd
cd backend
python app.py
```

### **Masalah: "No keys found" saat login**

**Solusi**: 
- Pastikan Anda sudah register terlebih dahulu
- Jangan hapus localStorage di browser
- Cek di Developer Tools → Application → Local Storage

---

## 📋 Checklist Sebelum Menjalankan

- [ ] Python 3.8+ sudah terinstall (`python --version`)
- [ ] Sudah masuk ke folder project
- [ ] Dependencies sudah terinstall (`pip install -r requirements.txt`)
- [ ] Sudah masuk ke folder `backend`
- [ ] Port 5000 tidak digunakan aplikasi lain

---

## 🎯 Quick Reference Commands

```cmd
# Masuk ke folder project
cd "d:\kuliah materi\CRYPTO\zkp-auth-system"

# Aktifkan virtual environment (opsional)
venv\Scripts\activate

# Install dependencies (hanya pertama kali)
pip install -r requirements.txt

# Masuk ke backend
cd backend

# Jalankan server
python app.py
```

---

## 📚 Dokumentasi Lainnya

- **README.md**: Dokumentasi lengkap sistem
- **TUTORIAL.md**: Tutorial step-by-step dengan penjelasan konsep
- **QUICKSTART.md**: Panduan cepat
- **CARA_JALANKAN.md**: Panduan detail (English)

---

## 🎉 Selamat!

Jika semua langkah berhasil, sistem ZKP Authentication Anda sudah berjalan!

**Penting**: 
- Private key **TIDAK PERNAH** dikirim ke server
- Hanya proof yang dikirim untuk verifikasi
- Ini adalah keajaiban Zero-Knowledge Proof! ✨

---

**Butuh Bantuan?** Pastikan semua checklist di atas sudah dicentang!

