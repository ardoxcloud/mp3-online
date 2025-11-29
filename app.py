import streamlit as st
import yt_dlp
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="MP3 Downloader", page_icon="🎵")
st.title("🎵 MP3 Downloader Online")
st.write("Masukkan Link YouTube, langsung jadi MP3!")

# --- FUNGSI DOWNLOAD ---
def download_mp3(url):
    # Buat folder sementara
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    # Konfigurasi yt-dlp dengan PENYAMARAN (Agar tidak error 403)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        # --- INI BAGIAN PENTINGNYA ---
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.youtube.com/',
        }
        # -----------------------------
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            judul = info.get('title', 'Audio')
            
            # Cari nama file aslinya
            filename = ydl.prepare_filename(info)
            # Ubah ekstensi manual ke mp3 untuk memastikan path benar
            final_filename = filename.rsplit('.', 1)[0] + ".mp3"
            
            return final_filename, judul
    except Exception as e:
        return None, str(e)

# --- TAMPILAN UTAMA ---
url = st.text_input("Paste Link YouTube di sini:")

if st.button("🚀 Proses Sekarang"):
    if url:
        with st.spinner("Sedang memproses... Tunggu sebentar..."):
            file_path, judul = download_mp3(url)
            
            if file_path and os.path.exists(file_path):
                st.success(f"Berhasil! Lagu: {judul}")
                
                # Baca file MP3
                with open(file_path, "rb") as f:
                    mp3_bytes = f.read()
                
                # MUNCULKAN TOMBOL DOWNLOAD
                st.download_button(
                    label="⬇️ DOWNLOAD MP3 KE HP/LAPTOP",
                    data=mp3_bytes,
                    file_name=os.path.basename(file_path),
                    mime="audio/mpeg"
                )
            else:
                # Jika error, tampilkan pesan merah
                st.error(f"Gagal memproses. Error: {judul}")
    else:
        st.warning("Link-nya mana?")
