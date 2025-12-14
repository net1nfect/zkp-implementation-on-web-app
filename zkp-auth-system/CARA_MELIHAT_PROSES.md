# 🔍 Cara Melihat Proses Kerja Sistem ZKP

## 📋 Daftar Isi

1. [Process Viewer (Visual Debug Panel)](#process-viewer)
2. [Browser Console Logging](#browser-console)
3. [Server Terminal Logging](#server-terminal)
4. [Step-by-Step Tracing](#step-by-step)
5. [Network Monitoring](#network-monitoring)

---

## 🎯 1. Process Viewer (Visual Debug Panel)

### **Cara Menggunakan:**

1. **Buka halaman login/register**
2. **Process Viewer akan muncul otomatis** di pojok kanan bawah
3. **Panel akan menampilkan:**
   - **Steps Tab**: Step-by-step proses yang sedang berjalan
   - **Data Tab**: Data yang digunakan (keys, proof, dll)
   - **Logs Tab**: Log messages real-time

### **Fitur Process Viewer:**

- ✅ **Real-time Updates**: Melihat setiap step saat terjadi
- ✅ **Visual Status**: 
  - ⏳ Pending (kuning)
  - ⚙️ Active (biru, berkedip)
  - ✅ Completed (hijau)
  - ❌ Error (merah)
- ✅ **Timing Info**: Waktu setiap step
- ✅ **Data Inspection**: Lihat nilai keys, proof, dll
- ✅ **Collapsible**: Bisa minimize/maximize

### **Contoh Penggunaan:**

**Saat Register:**
```
1. Input Username ✅
2. Generate Key Pair ⚙️ → ✅
3. Store Keys Locally ⚙️ → ✅
4. Send Public Key ⚙️ → ✅
```

**Saat Login:**
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

## 🖥️ 2. Browser Console Logging

### **Cara Menggunakan:**

1. **Tekan F12** di browser
2. **Pilih tab "Console"**
3. **Lihat log messages** saat proses berjalan

### **Log yang Akan Muncul:**

**Saat Register:**
```javascript
// Key generation
Using public key: {x: "0x...", y: "0x..."}
Username: idhamakbar

// Server response
Registration successful!
```

**Saat Login:**
```javascript
// Key loading
Using public key: {x: "0x...", y: "0x..."}
Username: idhamakbar

// Proof generation
Generated proof: {
  R: {x: "0x...", y: "0x..."},
  s: "0x...",
  c: "0x..."
}

// Server response
Login successful!
```

### **Cara Enable Detailed Logging:**

Tambahkan di console:
```javascript
// Enable verbose logging
localStorage.setItem('zkp_debug', 'true');
```

---

## 💻 3. Server Terminal Logging

### **Cara Menggunakan:**

1. **Buka terminal** tempat server berjalan
2. **Lihat output** saat request masuk

### **Log yang Akan Muncul:**

**Saat Register:**
```
POST /api/register
Username: idhamakbar
Public key received: x=0x..., y=0x...
User created successfully
```

**Saat Login:**
```
POST /api/login
Username: idhamakbar
DEBUG: Public key from DB - x: 0x..., y: 0x...
DEBUG: Proof received - R: {...}, s: 0x..., c: 0x...
DEBUG: Challenge from proof: 0x...
DEBUG: Challenge calculated: 0x...
DEBUG: Challenge match: True
DEBUG: left_side (s*G): x=0x..., y=0x...
DEBUG: right_side (R+c*Y): x=0x..., y=0x...
DEBUG: Points equal: True
Login successful!
```

---

## 📊 4. Step-by-Step Tracing

### **Registration Process:**

```
┌─────────────────────────────────────────┐
│ 1. User Input Username                  │
│    → "idhamakbar"                       │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 2. Browser Generate Key Pair            │
│    → privateKey = random(256-bit)       │
│    → publicKey = privateKey * G         │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 3. Store in localStorage                │
│    → zkp_private_key                    │
│    → zkp_public_key                     │
│    → zkp_username                       │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 4. Send to Server                       │
│    POST /api/register                   │
│    {username, public_key}               │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 5. Server Save to Database              │
│    → SQLite: users table                │
└─────────────────────────────────────────┘
```

### **Login Process (ZKP):**

```
┌─────────────────────────────────────────┐
│ 1. User Input Username                  │
│    → "idhamakbar"                       │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 2. Load Private Key                     │
│    → localStorage.getItem('zkp_...')   │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 3. Generate Random Nonce (r)            │
│    → r = random(1, CURVE_N-1)          │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 4. Compute Commitment (R)               │
│    → R = r * G                         │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 5. Generate Challenge (c)               │
│    → c = SHA256(R || Y || "auth") % n  │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 6. Compute Response (s)                 │
│    → s = (r + c * privateKey) % n      │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 7. Send Proof to Server                 │
│    POST /api/login                      │
│    {username, proof: {R, s, c}}        │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 8. Server Verification                 │
│    → Get public key from DB             │
│    → Verify: s*G == R + c*Y            │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 9. Create Session (if valid)            │
│    → Generate session token             │
│    → Store in Flask session             │
└─────────────────────────────────────────┘
```

---

## 🌐 5. Network Monitoring

### **Cara Menggunakan:**

1. **Tekan F12** → **Network tab**
2. **Filter: XHR** (untuk API calls)
3. **Lihat request/response**

### **Request yang Akan Terlihat:**

**Register:**
```
POST /api/register
Request:
{
  "username": "idhamakbar",
  "public_key": {
    "x": "0xab7c7ce7...",
    "y": "0x4c91d1c8..."
  }
}

Response:
{
  "message": "Registration successful",
  "user_id": 1,
  "username": "idhamakbar"
}
```

**Login:**
```
POST /api/login
Request:
{
  "username": "idhamakbar",
  "proof": {
    "R": {
      "x": "0x6c27f3a9...",
      "y": "0xa5f80dc7..."
    },
    "s": "0x86cea798...",
    "c": "0x33bf44c6..."
  }
}

Response:
{
  "message": "Login successful",
  "session_token": "...",
  "user": {...}
}
```

---

## 🎯 Quick Tips

### **1. Enable Verbose Logging:**
```javascript
// Di browser console
localStorage.setItem('zkp_debug', 'true');
```

### **2. Clear Process Viewer:**
```javascript
// Di browser console
processViewer.clear();
```

### **3. Inspect LocalStorage:**
```javascript
// Di browser console
console.log('Private Key:', localStorage.getItem('zkp_private_key'));
console.log('Public Key:', localStorage.getItem('zkp_public_key'));
console.log('Username:', localStorage.getItem('zkp_username'));
```

### **4. Monitor Server Logs:**
```bash
# Server akan print semua debug info
# Lihat terminal tempat server berjalan
```

---

## 📝 Checklist Monitoring

Saat testing, pastikan untuk melihat:

- [ ] **Process Viewer** - Step-by-step visual
- [ ] **Browser Console** - JavaScript logs
- [ ] **Server Terminal** - Python debug logs
- [ ] **Network Tab** - API requests/responses
- [ ] **LocalStorage** - Stored keys
- [ ] **Session Storage** - Session tokens

---

## 🎓 Contoh Lengkap

### **Scenario: Register & Login**

1. **Buka Process Viewer** (otomatis muncul)
2. **Register:**
   - Lihat step 1-4 di Process Viewer
   - Cek console untuk key generation
   - Cek network untuk API call
3. **Login:**
   - Lihat step 1-8 di Process Viewer
   - Cek console untuk proof generation
   - Cek server terminal untuk verification
   - Cek network untuk API call

---

**Dengan tools ini, Anda bisa melihat setiap detail proses ZKP authentication!** 🔍✨

