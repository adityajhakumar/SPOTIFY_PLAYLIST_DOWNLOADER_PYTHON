import streamlit as st
import subprocess
import os
import json
from pathlib import Path

# === CONFIG ===
st.set_page_config(page_title="Spotify Playlist Downloader", page_icon="🎵", layout="centered")
downloads_path = str(Path.home() / "Downloads" / "Spotify")
os.makedirs(downloads_path, exist_ok=True)

# === HEADER ===
st.markdown("""
<div style='text-align: center;'>
    <img src='https://upload.wikimedia.org/wikipedia/commons/2/26/Spotify_logo_with_text.svg' width='200'>
    <h2>🎧 Spotify Playlist Downloader</h2>
    <p style='color: gray;'>Download your Spotify playlist or album with fallback to YouTube</p>
</div>
""", unsafe_allow_html=True)

# === INPUT ===
playlist_url = st.text_input("🔗 Enter Spotify Playlist or Album URL", placeholder="https://open.spotify.com/...")
quality = st.selectbox("🎚️ Select MP3 Quality", ["320k", "192k", "128k"])

# === FUNCTION: Fetch playlist/album info ===
def get_playlist_tracks(playlist_url):
    temp_file = "temp.spotdl"
    try:
        subprocess.run(
            ["spotdl", "save", playlist_url, "--save-file", temp_file],
            capture_output=True, text=True, check=True
        )
        with open(temp_file, "r") as f:
            return json.load(f)
    except:
        return []
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

# === FUNCTION: Build detailed search query ===
def build_search_query(track):
    parts = []
    if 'name' in track: parts.append(track['name'])
    if 'artists' in track: parts.extend(track['artists'])
    if 'album_name' in track: parts.append(track['album_name'])
    return " ".join(parts)

# === FUNCTION: Download via spotDL ===
def download_with_spotdl(playlist_url, output_folder, quality):
    command = [
        "spotdl", "download", playlist_url,
        "--output", output_folder,
        "--format", "mp3",
        "--bitrate", quality,
        "--audio", "youtube", "soundcloud"
    ]
    return subprocess.run(command, capture_output=True, text=True)

# === FUNCTION: yt-dlp fallback (ytsearch5) ===
def fallback_download_ytdlp(search_query, output_folder):
    command = [
        "yt-dlp",
        f"ytsearch5:{search_query} audio",
        "-x", "--audio-format", "mp3",
        "--match-filter", "duration < 600",
        "-o", f"{output_folder}/%(title)s.%(ext)s"
    ]
    return subprocess.run(command, capture_output=True, text=True)

# === MAIN LOGIC ===
if playlist_url.strip():
    with st.spinner("🔍 Fetching playlist info..."):
        track_data = get_playlist_tracks(playlist_url)

        def extract_track_name(track):
            return (
                track.get("display_name")
                or track.get("name")
                or track.get("title")
                or track.get("url")
                or "Unknown Track"
            )

        track_names = [extract_track_name(t) for t in track_data]

    if track_names:
        st.success(f"📄 Playlist contains {len(track_names)} song(s)")
        with st.expander("🎵 View Track List"):
            for i, name in enumerate(track_names, 1):
                st.markdown(f"{i}. {name}")
    else:
        st.warning("⚠️ Could not fetch playlist. Please check the URL.")

    st.markdown(f"📁 Your songs will be saved to: `{downloads_path}`")

    if st.button("⬇️ Start Download"):
        st.info("🚀 Starting download...")
        with st.spinner("📥 Downloading via spotDL..."):
            result = download_with_spotdl(playlist_url, downloads_path, quality)

        # Detect failed downloads
        downloaded_files = os.listdir(downloads_path)
        failed_tracks = [name for name in track_names if not any(name[:10].lower() in file.lower() for file in downloaded_files)]

        if failed_tracks:
            st.warning(f"⚠️ {len(failed_tracks)} song(s) failed via spotDL. Retrying with yt-dlp...")
            with st.expander("🔁 Fallback to YouTube (yt-dlp)"):
                for i, (track, name) in enumerate(zip(track_data, track_names)):
                    if name in failed_tracks:
                        search_query = build_search_query(track)
                        with st.spinner(f"🎯 Searching YouTube for: {search_query}"):
                            res = fallback_download_ytdlp(search_query, downloads_path)
                            if res.returncode == 0:
                                st.success(f"✅ Fallback successful for: {name}")
                            else:
                                st.error(f"❌ Could not download: {name}")
        else:
            st.success("✅ All songs downloaded via spotDL!")

        st.success("🎉 Download complete! Check your Downloads/Spotify folder.")

# === LEGAL DISCLAIMER ===
st.markdown("""
<hr>
<div style='text-align: center; color: gray; font-size: small;'>
    <p>Built with ❤️ using <b>Streamlit</b>, <b>spotDL</b>, and <b>yt-dlp</b></p>
    <p><b>Disclaimer:</b> This application is developed solely for educational and personal use purposes. It is intended to demonstrate how open-source tools like <b>spotDL</b> and <b>yt-dlp</b> can be programmatically integrated using Python and Streamlit. We do not host, store, or redistribute any copyrighted content. This app does not bypass Spotify’s or YouTube’s protections or licensing systems and relies entirely on publicly available content. By using this application, you confirm that you are legally authorized to download the content you access, will not violate any terms of service, and accept that the developers are not responsible for any misuse or legal consequences. This tool is not intended for piracy, commercial use, or redistribution. Use it responsibly and at your own risk.</p>
""", unsafe_allow_html=True)
