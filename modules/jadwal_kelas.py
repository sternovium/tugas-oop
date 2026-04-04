class Matkul:
    def __init__(self, nama, dosen, ruangan, hari, jam_mulai, jam_selesai):
        self.nama        = nama
        self.dosen       = dosen
        self.ruangan     = ruangan
        self.hari        = hari
        self.jam_mulai   = jam_mulai
        self.jam_selesai = jam_selesai

    def info(self):
        return (
            f"  Mata Kuliah : {self.nama}\n"
            f"  Dosen       : {self.dosen}\n"
            f"  Ruangan     : {self.ruangan}\n"
            f"  Waktu       : {self.hari}, {self.jam_mulai} - {self.jam_selesai}"
        )

class JadwalKelas:
    def __init__(self, kelas):
        self.kelas         = kelas
        self.daftar_matkul = []

    def tambah_matkul(self, mata_kuliah):
        self.daftar_matkul.append(mata_kuliah)
        print(f"[+] '{mata_kuliah.nama}' berhasil ditambahkan.")

    def tampilkan_jadwal(self):
        print(f"\n{'='*45}")
        print(f"       JADWAL KELAS {self.kelas}")
        print(f"{'='*45}")
        if not self.daftar_matkul:
            print("  (Belum ada mata kuliah.)")
        for i, matkul in enumerate(self.daftar_matkul, 1):
            print(f"\n[{i}] {matkul.nama}")
            print(matkul.info())
        print(f"{'='*45}")

    def cari_jadwal(self, hari):
        print(f"\n--- Jadwal hari {hari} ---")
        hasil = [matkul for matkul in self.daftar_matkul if matkul.hari.lower() == hari.lower()]
        if not hasil:
            print("  Tidak ada kelas pada hari ini.")
        for matkul in hasil:
            print(f"\n  * {matkul.nama}")
            print(matkul.info())

    def hapus_matkul(self, nama):
        for matkul in self.daftar_matkul:
            if matkul.nama.lower() == nama.lower():
                self.daftar_matkul.remove(matkul)
                print(f"[-] '{matkul.nama}' berhasil dihapus.")
                return
        print(f"  Mata kuliah '{nama}' tidak ditemukan.")
