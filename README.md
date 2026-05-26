# 🎓 Repositori Kuliah OOP (Object-Oriented Programming) Python 🐍

Repositori ini berisi kumpulan tugas dan latihan (jobsheet) untuk mata kuliah **Object-Oriented Programming (OOP)** menggunakan bahasa pemrograman **Python**.

**Nama :** Naufal Azka Fadhlillah  
**NIM  :** 4.33.25.2.16  
**Institusi :** Politeknik Negeri Semarang

---

## 📂 Struktur Repositori

```
OOP/
├── jobsheet_01.ipynb       # Pengenalan OOP & Class Dasar
├── jobsheet_02.ipynb       # Atribut & Metode
├── jobsheet_03.ipynb       # Encapsulation
├── jobsheet_04.ipynb       # Inheritance (Pewarisan)
├── jobsheet_05.ipynb       # Polymorphism
├── jobsheet_06.ipynb       # Abstract Class & Interface
├── jobsheet_07.ipynb       # Exception Handling & File I/O
├── jobsheet_11/            # Aplikasi Catatan Pengeluaran (Streamlit)
│   ├── main_app.py         # Entry point – UI Streamlit
│   ├── manajer_anggaran.py # Logika bisnis (class AnggaranHarian)
│   ├── model.py            # Data model (class Transaksi)
│   ├── database.py         # Layer akses database SQLite
│   ├── konfigurasi.py      # Konstanta & konfigurasi aplikasi
│   └── pengeluaran_harian.db  # File database SQLite (auto-generated)
└── modules/                # Modul-modul pendukung
```

---

## 📒 Jobsheet 01–07 (Notebook)

File-file `.ipynb` berisi dokumentasi latihan dan praktik konsep dasar OOP secara bertahap, mulai dari pembuatan class sederhana hingga abstract class, polymorphism, dan exception handling.

**Cara membuka:**
- **VS Code** dengan ekstensi Jupyter
- **Jupyter Notebook / JupyterLab**
- **Google Colab** (upload file `.ipynb`)

---

## 💰 Jobsheet 11 – Aplikasi Catatan Pengeluaran Harian

Aplikasi web berbasis **Streamlit** untuk mencatat dan memantau pengeluaran harian. Dibangun dengan pendekatan OOP dan menggunakan **SQLite** sebagai penyimpanan data persisten.

### ✨ Fitur

| Fitur | Deskripsi |
|---|---|
| ➕ Tambah Transaksi | Input pengeluaran dengan deskripsi, kategori, jumlah, dan tanggal |
| 📋 Riwayat Transaksi | Tampilkan semua transaksi dalam tabel, lengkap dengan fitur hapus |
| 📊 Ringkasan | Total pengeluaran & breakdown per kategori (tabel + grafik batang) |
| 🔍 Filter Periode | Filter ringkasan berdasarkan hari ini, tanggal tertentu, atau semua waktu |
| 💾 Persistent Storage | Data tersimpan di database SQLite secara otomatis |

### 🏗️ Arsitektur

```
main_app.py (UI Layer – Streamlit)
     │
     ▼
manajer_anggaran.py (Business Logic – class AnggaranHarian)
     │
     ├── model.py   (Data Model – class Transaksi)
     └── database.py (Data Access Layer – SQLite)
                │
                └── konfigurasi.py (DB path, kategori)
```

### 📦 Kategori Pengeluaran

`Makanan` · `Transportasi` · `Hiburan` · `Tagihan` · `Belanja` · `Kesehatan` · `Pendidikan` · `Lainnya`

### 🚀 Cara Menjalankan

**1. Install dependensi**
```bash
pip install streamlit pandas
```

**2. Jalankan aplikasi**
```bash
py -m streamlit run jobsheet_11/main_app.py
```

**3. Buka browser**
```
http://localhost:8501
```

> 💡 Database (`pengeluaran_harian.db`) akan dibuat otomatis di folder `jobsheet_11/` saat pertama kali aplikasi dijalankan.

---

## 🛠️ Tech Stack

- **Python** – Bahasa utama
- **Streamlit** – Framework UI web
- **SQLite3** – Database lokal (built-in Python)
- **Pandas** – Manipulasi & tampilan data
- **OOP** – Desain berbasis class (`Transaksi`, `AnggaranHarian`)
