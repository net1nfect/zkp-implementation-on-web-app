# 🔧 Troubleshooting: "Invalid proof" Error

## ❌ Masalah

Saat login, muncul error: **"Login failed: Invalid proof"**

## 🔍 Penyebab Umum

### 1. **Username Mismatch** ⭐ (Paling Sering)

**Masalah**: Public key di localStorage tidak cocok dengan username yang digunakan untuk login.

**Contoh**:
- Anda register dengan username `alice` → public key disimpan di localStorage
- Lalu login dengan username `idhamakbar` → public key di localStorage berbeda dengan yang ada di database untuk `idhamakbar`

**Solusi**:
- Pastikan username yang digunakan untuk login **sama persis** dengan yang digunakan saat register
- Atau register ulang dengan username yang benar

### 2. **Public Key Tidak Cocok**

**Masalah**: Public key yang digunakan untuk generate proof berbeda dengan yang ada di database.

**Penyebab**:
- Register dengan username A, login dengan username B
- Database dihapus/reset, tapi localStorage masih ada
- Multiple registration dengan username yang sama

**Solusi**:
1. Hapus localStorage di browser:
   - Tekan F12 → Application → Local Storage → `http://localhost:5000`
   - Hapus semua item yang dimulai dengan `zkp_`
2. Register ulang dengan username yang benar

### 3. **Database Reset**

**Masalah**: Database dihapus/reset, tapi localStorage masih ada.

**Solusi**: Register ulang dengan username yang sama

## ✅ Langkah-langkah Perbaikan

### **Langkah 1: Cek Username**

Pastikan username yang digunakan untuk login **sama persis** dengan yang digunakan saat register (case-sensitive).

### **Langkah 2: Cek LocalStorage**

1. Tekan **F12** (Developer Tools)
2. Pilih tab **Application** (Chrome) atau **Storage** (Firefox)
3. Klik **Local Storage** → `http://localhost:5000`
4. Cek nilai `zkp_username`:
   - Harus sama dengan username yang digunakan untuk login
   - Jika berbeda, hapus semua item `zkp_*` dan register ulang

### **Langkah 3: Clear dan Register Ulang**

Jika masih error:

1. **Hapus localStorage**:
   - Di Developer Tools → Application → Local Storage
   - Klik kanan → Clear All
   - Atau hapus manual: `zkp_private_key`, `zkp_public_key`, `zkp_username`

2. **Hapus database** (opsional):
   - Hapus file `backend/zkp_auth.db`
   - Database akan dibuat ulang otomatis saat register

3. **Register ulang**:
   - Buka `http://localhost:5000/register`
   - Masukkan username yang benar
   - Klik "Generate Keys & Register"

4. **Login**:
   - Buka `http://localhost:5000/login`
   - Masukkan username yang **sama persis** dengan yang digunakan saat register
   - Klik "Generate Proof & Login"

## 🔍 Debug Mode

Saya sudah menambahkan logging di server. Cek console/terminal di mana server berjalan untuk melihat:
- Public key dari database
- Proof yang diterima
- Hasil verifikasi

## 📝 Checklist

Sebelum login, pastikan:
- [ ] Username sama persis dengan yang digunakan saat register
- [ ] Public key di localStorage sesuai dengan username
- [ ] Database tidak direset setelah register
- [ ] Tidak ada typo di username (case-sensitive)

## 🎯 Solusi Cepat

**Jika masih error, lakukan ini**:

```javascript
// Di browser console (F12 → Console), jalankan:
localStorage.clear();
```

Kemudian:
1. Register ulang dengan username yang benar
2. Login dengan username yang **sama persis**

---

**Masalah masih terjadi?** Cek console browser (F12) dan terminal server untuk melihat error detail.

