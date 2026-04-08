import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Downloader", page_icon="🎥")
st.title("YouTube Video Downloader 🎥")

url = st.text_input("Paste YouTube URL here:")

if url:
    try:
        # Step 1: Get Info
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            st.success(f"Found: {info.get('title')}")
            st.image(info.get('thumbnail'), width=300)

            if st.button("Download Video"):
                with st.spinner("Bypassing security and downloading..."):
                    out_filename = "video.mp4"
                    
                    # Updated options for 2026 security
                    ydl_opts = {
                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                        'outtmpl': out_filename,
                        'impersonate': 'chrome', # Requires curl-cffi in requirements
                        'extractor_args': {
                            'youtube': {
                                'player_client': ['android', 'web'],
                            }
                        }
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl_s:
                        ydl_s.download([url])
                    
                    if os.path.exists(out_filename):
                        with open(out_filename, "rb") as f:
                            st.download_button("💾 Save to Device", f, file_name=f"{info.get('title')}.mp4")
                        os.remove(out_filename)

    except Exception as e:
        st.error(f"Error: {e}")
