# main_app.py
import streamlit as st
import datetime
import pandas as pd
import locale

# ── Locale (format Rupiah) ──────────────────────────────────────────────────
try:
    locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'Indonesian_Indonesia.1252')
    except Exception:
        pass  # Locale tidak tersedia, gunakan fallback


def format_rp(angka: float) -> str:
    try:
        return locale.currency(angka or 0, grouping=True, symbol='Rp ')[:-3]
    except Exception:
        return f"Rp {angka or 0:,.0f}".replace(",", ".")


# ── Import modul backend ────────────────────────────────────────────────────
try:
    from model import Transaksi
    from manajer_anggaran import AnggaranHarian
    from konfigurasi import KATEGORI_PENGELUARAN
except ImportError as e:
    st.error(f"Gagal mengimpor modul: {e}. Pastikan semua file .py ada dalam satu folder.")
    st.stop()

# ── Konfigurasi halaman ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Catatan Pengeluaran",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Inisialisasi AnggaranHarian (di-cache agar tidak reload terus) ──────────
@st.cache_resource
def get_anggaran_manager() -> AnggaranHarian:
    print(">>> STREAMLIT: (Cache Resource) Menginisialisasi AnggaranHarian...")
    return AnggaranHarian()


anggaran = get_anggaran_manager()


# ════════════════════════════════════════════════════════════════════════════
#  HALAMAN 1 – TAMBAH TRANSAKSI
# ════════════════════════════════════════════════════════════════════════════
def halaman_input(mgr: AnggaranHarian):
    st.header("💸 Tambah Pengeluaran Baru")

    with st.form("form_transaksi_baru", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            deskripsi = st.text_input("Deskripsi*", placeholder="Contoh: Makan siang")
        with col2:
            kategori = st.selectbox("Kategori*:", KATEGORI_PENGELUARAN, index=0)

        col3, col4 = st.columns([1, 1])
        with col3:
            jumlah = st.number_input(
                "Jumlah (Rp)*:", min_value=0.01, step=1000.0,
                format="%.0f", value=None, placeholder="Contoh: 25000"
            )
        with col4:
            tanggal = st.date_input("Tanggal*:", value=datetime.date.today())

        submitted = st.form_submit_button("💾 Simpan Transaksi")

    if submitted:
        if not deskripsi:
            st.warning("⚠️ Deskripsi wajib diisi!")
        elif jumlah is None or jumlah <= 0:
            st.warning("⚠️ Jumlah wajib diisi dan harus lebih dari 0!")
        else:
            with st.spinner("Menyimpan..."):
                tx = Transaksi(deskripsi, float(jumlah), kategori, tanggal)
                if mgr.tambah_transaksi(tx):
                    st.success(f"✅ Transaksi '{deskripsi}' berhasil disimpan!", icon="✅")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("❌ Gagal menyimpan transaksi. Periksa terminal.", icon="❌")


# ════════════════════════════════════════════════════════════════════════════
#  HALAMAN 2 – RIWAYAT TRANSAKSI (dengan fitur Hapus)
# ════════════════════════════════════════════════════════════════════════════
def halaman_riwayat(mgr: AnggaranHarian):
    st.header("📋 Riwayat Transaksi")

    col_refresh, _ = st.columns([1, 5])
    with col_refresh:
        if st.button("🔄 Refresh"):
            st.cache_data.clear()
            st.rerun()

    # ── Tampilkan tabel ──
    with st.spinner("Memuat riwayat..."):
        df = mgr.get_dataframe_transaksi()

    if df is None:
        st.error("Gagal mengambil data riwayat.")
        return
    if df.empty:
        st.info("Belum ada transaksi yang tercatat.")
        return

    st.dataframe(df, use_container_width=True, hide_index=True)

    # ── Panel Hapus Transaksi (Penugasan) ────────────────────────────────
    st.divider()
    st.subheader("🗑️ Hapus Transaksi")

    # Ambil semua ID yang tersedia untuk dropdown
    id_list = df['id'].tolist()
    id_options = {f"ID {row['id']} | {row['tanggal']} | {row['deskripsi']} | {row['Jumlah (Rp)']}": row['id']
                  for _, row in df.iterrows()}

    pilihan_label = st.selectbox(
        "Pilih transaksi yang ingin dihapus:",
        options=list(id_options.keys()),
        key="select_hapus"
    )
    id_terpilih = id_options[pilihan_label]

    st.warning(f"⚠️ Anda akan menghapus: **{pilihan_label}**")

    # Dua tombol: konfirmasi dan batal
    col_hapus, col_batal, _ = st.columns([1, 1, 4])
    with col_hapus:
        konfirmasi = st.button("🗑️ Konfirmasi Hapus", type="primary")
    with col_batal:
        batal = st.button("↩️ Batal")

    if konfirmasi:
        with st.spinner("Menghapus..."):
            berhasil = mgr.hapus_transaksi(int(id_terpilih))
        if berhasil:
            st.success(f"✅ Transaksi ID {id_terpilih} berhasil dihapus!")
            st.cache_data.clear()
            st.rerun()
        else:
            st.error("❌ Gagal menghapus transaksi. Periksa terminal.")
    if batal:
        st.info("Penghapusan dibatalkan.")


# ════════════════════════════════════════════════════════════════════════════
#  HALAMAN 3 – RINGKASAN
# ════════════════════════════════════════════════════════════════════════════
def halaman_ringkasan(mgr: AnggaranHarian):
    st.header("📊 Ringkasan Pengeluaran")

    col_filter1, col_filter2 = st.columns([1, 2])

    with col_filter1:
        pilihan_periode = st.selectbox(
            "Filter Periode:",
            ["Semua Waktu", "Hari Ini", "Pilih Tanggal"],
            key="filter_periode",
            on_change=lambda: st.cache_data.clear()
        )

    tanggal_filter = None
    label_periode = "(Semua Waktu)"

    if pilihan_periode == "Hari Ini":
        tanggal_filter = datetime.date.today()
        label_periode = f"({tanggal_filter.strftime('%d %b %Y')})"

    elif pilihan_periode == "Pilih Tanggal":
        if 'tanggal_pilihan_state' not in st.session_state:
            st.session_state.tanggal_pilihan_state = datetime.date.today()
        tanggal_filter = st.date_input(
            "Pilih Tanggal:",
            value=st.session_state.tanggal_pilihan_state,
            key="tanggal_pilihan"
        )
        st.session_state.tanggal_pilihan_state = tanggal_filter
        label_periode = f"({tanggal_filter.strftime('%d %b %Y')})"
        st.cache_data.clear()

    # ── Metrik total ──
    with col_filter2:
        @st.cache_data(ttl=300)
        def hitung_total_cached(tgl):
            return mgr.hitung_total_pengeluaran(tanggal=tgl)

        total = hitung_total_cached(tanggal_filter)
        st.metric(label=f"💰 Total Pengeluaran {label_periode}", value=format_rp(total))

    st.divider()

    # ── Per Kategori ──
    st.subheader(f"Pengeluaran per Kategori {label_periode}")

    @st.cache_data(ttl=300)
    def get_kategori_cached(tgl):
        return mgr.get_pengeluaran_per_kategori(tanggal=tgl)

    with st.spinner("Memuat ringkasan kategori..."):
        dict_kategori = get_kategori_cached(tanggal_filter)

    if not dict_kategori:
        st.info("Tidak ada data untuk periode ini.")
    else:
        try:
            data_kat = [{"Kategori": k, "Total": v} for k, v in dict_kategori.items()]
            df_kat = (
                pd.DataFrame(data_kat)
                .sort_values(by="Total", ascending=False)
                .reset_index(drop=True)
            )
            df_kat['Total (Rp)'] = df_kat['Total'].apply(format_rp)

            col_kat1, col_kat2 = st.columns(2)
            with col_kat1:
                st.write("**Tabel:**")
                st.dataframe(df_kat[['Kategori', 'Total (Rp)']], hide_index=True,
                             use_container_width=True)
            with col_kat2:
                st.write("**Grafik:**")
                st.bar_chart(df_kat.set_index('Kategori')['Total'],
                             use_container_width=True)
        except Exception as e:
            st.error(f"Gagal menampilkan ringkasan: {e}")


# ════════════════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════════════════
def main():
    st.sidebar.title("💰 Catatan Pengeluaran")
    menu = st.sidebar.radio(
        "Pilih Menu:",
        ["Tambah", "Riwayat", "Ringkasan"],
        key="menu_utama"
    )
    st.sidebar.markdown("---")
    st.sidebar.info("Jobsheet 11 – Aplikasi Keuangan OOP")

    mgr = get_anggaran_manager()

    if menu == "Tambah":
        halaman_input(mgr)
    elif menu == "Riwayat":
        halaman_riwayat(mgr)
    elif menu == "Ringkasan":
        halaman_ringkasan(mgr)

    st.markdown("---")
    st.caption("Pengembangan Aplikasi Berbasis OOP | Politeknik Negeri Semarang")


if __name__ == "__main__":
    main()
