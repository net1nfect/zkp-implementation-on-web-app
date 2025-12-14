# ⚡ Quick Guide: Melihat Proses Kerja Sistem

## 🎯 Cara Cepat

### **1. Process Viewer (Paling Mudah)**

**Langkah:**
1. Buka halaman login/register
2. **Process Viewer muncul otomatis** di pojok kanan bawah
3. Klik tab **"Steps"** untuk melihat step-by-step
4. Klik tab **"Data"** untuk melihat keys dan proof
5. Klik tab **"Logs"** untuk melihat log messages

**Fitur:**
- ✅ Real-time updates
- ✅ Visual status (pending/active/completed/error)
- ✅ Timing information
- ✅ Data inspection

---

### **2. Browser Console (F12)**

**Langkah:**
1. Tekan **F12**
2. Pilih tab **"Console"**
3. Lihat log saat proses berjalan

**Yang Akan Terlihat:**
- Key generation logs
- Proof generation logs
- Error messages

---

### **3. Server Terminal**

**Langkah:**
1. Lihat terminal tempat server berjalan
2. Lihat output saat request masuk

**Yang Akan Terlihat:**
- Public key dari database
- Proof verification details
- Challenge comparison
- Verification result

---

## 📊 Visual Process Flow

### **Registration:**
```
1. Input Username ✅
2. Generate Key Pair ⚙️ → ✅
3. Store Keys Locally ⚙️ → ✅
4. Send Public Key ⚙️ → ✅
```

### **Login (ZKP):**
```
1. Input Username ✅
2. Load Private Key ⚙️ → ✅
3. Generate Random Nonce ⚙️ → ✅
4. Compute Commitment ⚙️ → ✅
5. Generate Challenge ⚙️ → ✅
6. Compute Response ⚙️ → ✅
7. Send Proof ⚙️ → ✅
8. Server Verification ⚙️ → ✅
```

---

## 🎓 Tips

1. **Process Viewer bisa di-minimize** - Klik tombol "−" di header
2. **Auto-scroll** - Logs otomatis scroll ke bawah
3. **Clear logs** - Refresh page untuk clear
4. **Multiple tabs** - Bisa buka Steps, Data, dan Logs bersamaan

---

**Sekarang Anda bisa melihat setiap detail proses ZKP!** 🔍✨

