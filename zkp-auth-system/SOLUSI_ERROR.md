# 🔧 Solusi Error: "ModuleNotFoundError: No module named 'flask'"

## ❌ Masalah

Anda mendapat error:
```
ModuleNotFoundError: No module named 'flask'
```

## 🔍 Penyebab

Anda memiliki **dua instalasi Python**:
1. **Python System** (Python 3.13.7) - Flask sudah terinstall di sini
2. **Python MSYS2** (`C:\msys64\mingw64\bin\python.exe`) - Flask belum terinstall

Saat Anda mengetik `python`, sistem menggunakan Python MSYS2 yang belum punya Flask.

## ✅ Solusi

### **Opsi 1: Gunakan `py` Launcher** ⭐ (Paling Mudah)

Gunakan `py` instead of `python`:

```powershell
cd backend
py app.py
```

**Atau** double-click file `run_app.bat` di folder `backend`.

---

### **Opsi 2: Install Flask ke Python MSYS2**

Jika Anda ingin tetap menggunakan `python`, install Flask ke Python MSYS2:

```powershell
# Cek Python yang digunakan
python --version

# Install Flask (jika pip tersedia)
python -m pip install Flask SQLAlchemy Werkzeug
```

**Catatan**: Python MSYS2 mungkin tidak punya pip. Jika error, gunakan Opsi 1.

---

### **Opsi 3: Gunakan Full Path ke Python System**

Cari lokasi Python system Anda:
```powershell
where py
```

Kemudian gunakan full path:
```powershell
C:\Users\akbarsigma\AppData\Local\Programs\Python\Python313\python.exe app.py
```

---

## 🎯 Rekomendasi

**Gunakan `py` launcher** karena:
- ✅ Otomatis menggunakan Python yang benar
- ✅ Flask sudah terinstall
- ✅ Lebih mudah dan konsisten

## 📝 Command yang Benar

```powershell
# Masuk ke folder backend
cd "d:\kuliah materi\CRYPTO\zkp-auth-system\backend"

# Jalankan dengan py
py app.py
```

Atau gunakan script `run_app.bat`:
```powershell
cd backend
.\run_app.bat
```

---

## ✅ Verifikasi

Untuk memastikan Flask terinstall, jalankan:
```powershell
py -c "import flask; print('Flask OK!')"
```

Jika output: `Flask OK!` → Siap digunakan! 🎉

---

**Setelah menggunakan `py app.py`, server akan berjalan di `http://localhost:5000`**

