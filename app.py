import streamlit as st
import yt_dlp
import os
import time

# --- JUDUL WEBSITE ---
st.set_page_config(page_title="MP3 Downloader Online", page_icon="🎵")
st.title("🎵 MP3 Downloader Online")
st.write("Copy link YouTube, paste di bawah, download MP3-nya. Gratis!")

# --- FUNGSI DOWNLOAD ---
def download_mp3(url):
    # Buat folder sementara di server
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    # Opsi yt-dlp (Tanpa FFmpeg path khusus, karena di server biasanya sudah auto)
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
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            judul = info.get('title', 'Audio')
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
            return filename, judul
            
    except Exception as e:
        st.error(f"Error: {e}")
        return None, None

# --- INPUT USER ---
url = st.text_input("Paste Link YouTube di sini:")

if st.button("🚀 Proses ke MP3"):
    if url:
        with st.spinner("Sedang mendownload & konversi di server..."):
            file_path, judul = download_mp3(url)
            
            if file_path and os.path.exists(file_path):
                st.success(f"Berhasil! Lagu: {judul}")
                
                # BACA FILE MP3 AGAR BISA DIDOWNLOAD USER
                with open(file_path, "rb") as f:
                    mp3_bytes = f.read()
                
                # TOMBOL DOWNLOAD AKHIR
                st.download_button(
                    label="⬇️ DOWNLOAD MP3 SEKARANG",
                    data=mp3_bytes,
                    file_name=os.path.basename(file_path),
                    mime="audio/mpeg"
                )
                
                # Bersihkan file di server agar storage tidak penuh
                os.remove(file_path)
            else:
                st.error("Gagal memproses file.")
    else:
        st.warning("Masukkan link dulu dong!")