# 🔥 Force Process Killer - Bloatware Terminator v2.0

(Preview at the bottom)

A powerful Python script designed to aggressively terminate stubborn processes and bloatware that refuse to close normally. Perfect for cleaning up system resources and eliminating persistent background applications.

## ⚡ Features

### 🎯 **Multiple Operation Modes**
- **Interactive Process Manager** - Browse, search, and manually kill processes
- **Standard Auto Kill** - Clean termination with cache cleanup (Defender-safe)
- **Nuclear Mode** - Extreme termination with Windows Defender shutdown

### 🔍 **Process Management**
- Real-time process scanning with CPU and memory usage
- Search functionality for specific processes
- Protected system process detection
- Target process marking and identification

### 💀 **Advanced Termination Methods**
- **Phase 1**: Gentle termination (standard)
- **Phase 2**: Force kill (aggressive)
- **Phase 3**: Taskkill command (system-level)
- **Phase 4**: Nuclear mode (multi-method spam attack)

### 🧹 **System Cleanup**
- Automatic memory cleanup and optimization
- Cache clearing (DNS, ARP, NetBios, Temp files)
- Windows prefetch and log cleanup
- Memory compaction for better performance

### 🛡️ **Windows Defender Control** (Nuclear Mode Only)
- Complete real-time protection disabling
- Registry modifications for persistent disabling
- Service termination and startup disabling
- Tamper protection bypass

## 🎯 Target Processes

The script targets common bloatware and resource-heavy applications:

### Browsers
- Chrome, Edge, Firefox, Brave
- Edge WebView2 (stubborn process)

### Communication & Media
- Microsoft Teams, Skype, Discord
- Spotify, WhatsApp

### Development & Creative
- Adobe services and updaters
- Office Click-to-Run

### Gaming Platforms
- Steam, Origin, Epic Games Launcher
- Xbox services

### Security Software
- Third-party antivirus (Avast, AVG, McAfee)
- Windows Defender components (Nuclear mode only)

### System Services
- Windows Search Indexer
- Print Spooler
- Windows Widgets

## 🚀 Installation & Usage

### Prerequisites
```bash
# Python 3.6 or higher required
# psutil will be auto-installed if missing
```

### Quick Start
1. **Download** the script
2. **Run as Administrator** (recommended for best results)
```bash
python force_kill_bloatware.py
```
3. **Choose your mode**:
   - Option 1: Interactive management
   - Option 2: Standard auto-kill (safe)
   - Option 3: Nuclear mode (extreme)

### Auto-Installation
The script automatically installs required dependencies:
- Detects missing `psutil` library
- Auto-installs via pip
- Handles installation errors gracefully

## 📋 Menu Options

### 1. Interactive Process Manager
- **View all processes** with resource usage
- **Search specific processes** by name
- **Manual process selection** and termination
- **Protected process warnings**

### 2. Standard Auto Kill (Recommended)
- Terminates all target processes safely
- **Preserves Windows Defender** functionality
- Includes memory and cache cleanup
- Safe for daily use

### 3. Nuclear Mode (⚠️ EXTREME)
- **Requires typing 'NUKE' to confirm**
- **Administrator privileges mandatory**
- Complete Windows Defender shutdown
- Registry modifications
- Multi-method spam attacks on stubborn processes
- Maximum system cleanup

## 🛡️ Safety Features

### Protected Processes
The script protects critical system processes:
- `explorer.exe`, `csrss.exe`, `winlogon.exe`
- `services.exe`, `lsass.exe`, `svchost.exe`
- Other essential Windows components

### Error Handling
- Comprehensive exception handling
- Timeout protection for all operations
- Safe subprocess execution
- Progress indicators and status reporting

### User Confirmation
- Clear warnings for destructive operations
- Confirmation prompts for Nuclear mode
- Administrator privilege detection
- Operation cancellation options

## 🔧 Technical Details

### Nuclear Kill Algorithm
For extremely stubborn processes like `msedgewebview2.exe`:
1. **Multi-signal attack**: SIGTERM, SIGKILL, SIGINT, SIGHUP
2. **System-level termination**: taskkill with various flags
3. **WMI termination**: Windows Management Interface
4. **PowerShell termination**: Alternative method
5. **Loop until dead**: Up to 50 attempts with verification

### Memory Cleanup Process
1. **Cache clearing**: DNS, ARP, routing tables
2. **Temporary file removal**: Windows temp, user temp, prefetch
3. **Log cleanup**: Event logs, error reports
4. **Memory compaction**: Process working set optimization
5. **Garbage collection**: .NET framework cleanup

### Windows Defender Shutdown (Nuclear Mode)
1. **Service termination**: Multiple methods for each service
2. **PowerShell commands**: 15+ disabling commands
3. **Registry modifications**: 13 critical registry keys
4. **Tamper protection bypass**: Advanced registry tweaks
5. **Persistent disabling**: Startup type modifications

## ⚠️ Warnings & Disclaimers

### ⚠️ **Nuclear Mode Risks**
- May cause temporary system instability
- Disables Windows security features
- Requires system restart to fully restore Defender
- Use only when absolutely necessary

### ⚠️ **General Precautions**
- **Save your work** before running
- **Close important applications** manually first
- **Run as Administrator** for best results
- **Not recommended on production servers**

### ⚠️ **Compatibility**
- **Windows 10/11 only**
- Requires PowerShell execution rights
- Some features need Administrator privileges

## 🐛 Troubleshooting

### Common Issues

**Script crashes during nuclear kill:**
- Fixed in v2.0 with enhanced error handling
- All subprocess calls now have timeouts
- Safe progress indicators implemented

**Process won't die:**
- Try Nuclear mode for stubborn processes
- Ensure Administrator privileges
- Some processes may restart automatically

**Permission denied errors:**
- Run as Administrator
- Check antivirus interference
- Disable real-time protection temporarily

**psutil installation fails:**
- Check internet connection
- Try manual installation: `pip install psutil`
- Update pip: `python -m pip install --upgrade pip`

## 📈 Performance Impact

### Before Cleanup
- High memory usage from bloatware
- Slow system responsiveness
- Multiple background processes

### After Cleanup
- Reduced memory footprint
- Improved system performance
- Cleaner process list
- Optimized cache and temporary files

## 🔄 Version History

### v2.0 (Current)
- ✅ Fixed CMD force close issue
- ✅ Enhanced nuclear kill methods
- ✅ Comprehensive error handling
- ✅ Memory and cache cleanup system
- ✅ Improved Windows Defender shutdown
- ✅ Safe subprocess execution
- ✅ Interactive process management

### v1.0 
- Basic process termination
- Simple target list
- Manual psutil installation required

## 📝 License

This project is provided as-is for educational and personal use. Use at your own risk.

## 🤝 Contributing

Feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Share improvement ideas

## ⭐ Show Your Support

If this tool helped you reclaim your system resources, please consider:
- ⭐ Starring this repository
- 🍴 Forking for your modifications
- 📢 Sharing with others who need it
- 🐛 Reporting bugs to help improve it

---

**Remember: With great power comes great responsibility. Use wisely!** 🕷️

---

# 🔥 Force Process Killer - Bloatware Terminator v2.0

Sebuah script Python yang powerful untuk menghentikan proses-proses bandel dan bloatware yang menolak untuk ditutup secara normal. Sempurna untuk membersihkan resource sistem dan menghilangkan aplikasi background yang persisten.

## ⚡ Fitur Utama

### 🎯 **Multiple Mode Operasi**
- **Interactive Process Manager** - Browse, cari, dan kill proses secara manual
- **Standard Auto Kill** - Terminasi bersih dengan pembersihan cache (aman untuk Defender)
- **Nuclear Mode** - Terminasi ekstrem dengan shutdown Windows Defender

### 🔍 **Manajemen Proses**
- Scanning proses real-time dengan info CPU dan memory
- Fungsi pencarian untuk proses spesifik
- Deteksi proses sistem yang dilindungi
- Penandaan dan identifikasi proses target

### 💀 **Metode Terminasi Advanced**
- **Phase 1**: Terminasi lembut (standard)
- **Phase 2**: Force kill (agresif)
- **Phase 3**: Perintah taskkill (level sistem)
- **Phase 4**: Nuclear mode (serangan spam multi-metode)

### 🧹 **Pembersihan Sistem**
- Pembersihan memory otomatis dan optimisasi
- Pembersihan cache (DNS, ARP, NetBios, file temp)
- Pembersihan Windows prefetch dan log
- Kompaksi memory untuk performa lebih baik

### 🛡️ **Kontrol Windows Defender** (Hanya Nuclear Mode)
- Penonaktifan real-time protection lengkap
- Modifikasi registry untuk disable persisten
- Terminasi service dan disable startup
- Bypass tamper protection

## 🎯 Target Proses

Script ini menargetkan bloatware umum dan aplikasi yang boros resource:

### Browser
- Chrome, Edge, Firefox, Brave
- Edge WebView2 (proses bandel)

### Komunikasi & Media
- Microsoft Teams, Skype, Discord
- Spotify, WhatsApp

### Development & Creative
- Service Adobe dan updater
- Office Click-to-Run

### Platform Gaming
- Steam, Origin, Epic Games Launcher
- Service Xbox

### Software Security
- Antivirus third-party (Avast, AVG, McAfee)
- Komponen Windows Defender (hanya Nuclear mode)

### Service Sistem
- Windows Search Indexer
- Print Spooler
- Windows Widgets

## 🚀 Instalasi & Penggunaan

### Prasyarat
```bash
# Python 3.6 atau lebih tinggi diperlukan
# psutil akan auto-install jika tidak ada
```

### Quick Start
1. **Download** script
2. **Jalankan sebagai Administrator** (direkomendasikan untuk hasil terbaik)
```bash
python force_kill_bloatware.py
```
3. **Pilih mode Anda**:
   - Opsi 1: Manajemen interaktif
   - Opsi 2: Standard auto-kill (aman)
   - Opsi 3: Nuclear mode (ekstrem)

### Auto-Installation
Script otomatis menginstall dependencies yang diperlukan:
- Mendeteksi library `psutil` yang hilang
- Auto-install via pip
- Menangani error instalasi dengan baik

## 📋 Opsi Menu

### 1. Interactive Process Manager
- **Lihat semua proses** dengan penggunaan resource
- **Cari proses spesifik** berdasarkan nama
- **Seleksi proses manual** dan terminasi
- **Peringatan proses yang dilindungi**

### 2. Standard Auto Kill (Direkomendasikan)
- Menghentikan semua proses target dengan aman
- **Mempertahankan fungsionalitas Windows Defender**
- Termasuk pembersihan memory dan cache
- Aman untuk penggunaan harian

### 3. Nuclear Mode (⚠️ EKSTREM)
- **Memerlukan mengetik 'NUKE' untuk konfirmasi**
- **Hak Administrator wajib**
- Shutdown Windows Defender lengkap
- Modifikasi registry
- Serangan spam multi-metode pada proses bandel
- Pembersihan sistem maksimal

## 🛡️ Fitur Keamanan

### Proses yang Dilindungi
Script melindungi proses sistem kritis:
- `explorer.exe`, `csrss.exe`, `winlogon.exe`
- `services.exe`, `lsass.exe`, `svchost.exe`
- Komponen Windows essensial lainnya

### Error Handling
- Exception handling yang komprehensif
- Proteksi timeout untuk semua operasi
- Eksekusi subprocess yang aman
- Indikator progress dan pelaporan status

### Konfirmasi User
- Peringatan jelas untuk operasi destruktif
- Prompt konfirmasi untuk Nuclear mode
- Deteksi hak Administrator
- Opsi pembatalan operasi

## 🔧 Detail Teknis

### Algoritma Nuclear Kill
Untuk proses yang sangat bandel seperti `msedgewebview2.exe`:
1. **Serangan multi-signal**: SIGTERM, SIGKILL, SIGINT, SIGHUP
2. **Terminasi level sistem**: taskkill dengan berbagai flag
3. **Terminasi WMI**: Windows Management Interface
4. **Terminasi PowerShell**: Metode alternatif
5. **Loop sampai mati**: Hingga 50 percobaan dengan verifikasi

### Proses Pembersihan Memory
1. **Pembersihan cache**: DNS, ARP, routing tables
2. **Penghapusan file sementara**: Windows temp, user temp, prefetch
3. **Pembersihan log**: Event logs, error reports
4. **Kompaksi memory**: Optimisasi working set proses
5. **Garbage collection**: Pembersihan .NET framework

### Shutdown Windows Defender (Nuclear Mode)
1. **Terminasi service**: Multiple metode untuk setiap service
2. **Perintah PowerShell**: 15+ perintah disable
3. **Modifikasi registry**: 13 registry key kritis
4. **Bypass tamper protection**: Registry tweaks advanced
5. **Disable persisten**: Modifikasi startup type

## ⚠️ Peringatan & Disclaimer

### ⚠️ **Risiko Nuclear Mode**
- Dapat menyebabkan ketidakstabilan sistem sementara
- Menonaktifkan fitur keamanan Windows
- Memerlukan restart sistem untuk restore Defender sepenuhnya
- Gunakan hanya jika benar-benar diperlukan

### ⚠️ **Pencegahan Umum**
- **Simpan pekerjaan Anda** sebelum menjalankan
- **Tutup aplikasi penting** secara manual terlebih dahulu
- **Jalankan sebagai Administrator** untuk hasil terbaik
- **Tidak direkomendasikan pada server produksi**

### ⚠️ **Kompatibilitas**
- **Windows 10/11 saja**
- Memerlukan hak eksekusi PowerShell
- Beberapa fitur memerlukan hak Administrator

## 🐛 Troubleshooting

### Masalah Umum

**Script crash saat nuclear kill:**
- Diperbaiki di v2.0 dengan enhanced error handling
- Semua panggilan subprocess sekarang memiliki timeout
- Implementasi indikator progress yang aman

**Proses tidak mau mati:**
- Coba Nuclear mode untuk proses bandel
- Pastikan hak Administrator
- Beberapa proses mungkin restart otomatis

**Error permission denied:**
- Jalankan sebagai Administrator
- Cek interferensi antivirus
- Disable real-time protection sementara

**Instalasi psutil gagal:**
- Cek koneksi internet
- Coba instalasi manual: `pip install psutil`
- Update pip: `python -m pip install --upgrade pip`

## 📈 Dampak Performa

### Sebelum Cleanup
- Penggunaan memory tinggi dari bloatware
- Responsivitas sistem lambat
- Multiple proses background

### Setelah Cleanup
- Footprint memory berkurang
- Performa sistem meningkat
- Daftar proses lebih bersih
- Cache dan file sementara teroptimisasi

## 🔄 Riwayat Versi

### v2.0 (Saat ini)
- ✅ Perbaikan masalah CMD force close
- ✅ Enhanced nuclear kill methods
- ✅ Error handling komprehensif
- ✅ Sistem pembersihan memory dan cache
- ✅ Peningkatan shutdown Windows Defender
- ✅ Eksekusi subprocess yang aman
- ✅ Manajemen proses interaktif

### v1.0 
- Terminasi proses dasar
- Daftar target sederhana
- Instalasi psutil manual diperlukan

## 📝 Lisensi

Proyek ini disediakan apa adanya untuk penggunaan edukasi dan personal. Gunakan dengan risiko sendiri.

## 🤝 Kontribusi

Silakan untuk:
- Melaporkan bug dan issues
- Menyarankan fitur baru
- Submit pull requests
- Berbagi ide perbaikan

## ⭐ Tunjukkan Dukungan Anda

Jika tool ini membantu Anda merebut kembali resource sistem, mohon pertimbangkan:
- ⭐ Star repository ini
- 🍴 Fork untuk modifikasi Anda
- 📢 Share dengan orang lain yang membutuhkan
- 🐛 Laporkan bug untuk membantu perbaikan

---

**Ingat: Dengan kekuatan besar datang tanggung jawab besar. Gunakan dengan bijak!** 🕷️

<img width="761" height="459" alt="image" src="https://github.com/user-attachments/assets/653076d3-fdec-4720-a883-9ea87f67ed8a" />

<img width="619" height="263" alt="image" src="https://github.com/user-attachments/assets/63deb992-e0df-4017-866b-5d7e8ac2d468" />

<img width="677" height="174" alt="image" src="https://github.com/user-attachments/assets/b8162108-9040-4b26-b081-afddbe04476d" />


