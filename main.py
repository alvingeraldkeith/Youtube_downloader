import streamlit as st
import yt_dlp
import os

# --- 1. CONFIG & SESSION SETUP ---
st.set_page_config(page_title="Universal YT Downloader", page_icon="📺")

# Create the cookie file from Streamlit Secrets if it exists
# This bypasses the 403 Forbidden error globally
if "YOUTUBE_COOKIES" in st.secrets:
    with open("temp_cookies.txt", "w") as f:
        f.write(st.secrets["YOUTUBE_COOKIES"])

st.title("Universal YouTube Downloader 🎥")
st.write("Stable version with secure authentication and quality selection.")

# --- 2. USER INPUT ---
url = st.text_input("Paste YouTube Link here:", placeholder="https://www.youtube.com/...")

if url:
    try:
        # Step 1: Fetch metadata using your cookies
        ydl_info_opts = {
            'quiet': True,
            'no_warnings': True,
            'cookiefile': 'temp_cookies.txt' if os.path.exists("temp_cookies.txt") else None
        }
        
        with yt_dlp.YoutubeDL(ydl_info_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video')
            st.success(f"Ready: **{title}**")
            st.image(info.get('thumbnail'), width=300)

        # Step 2: Quality Selection
        # We stick to single-file formats (<=720p) to avoid merging errors
        option = st.selectbox("Select Quality:", ["720p (HD)", "360p (Data Saver)"])
        max_height = "720" if "720p" in option else "360"

        # Step 3: Download Logic
        if st.button("Generate Download Link"):
            with st.spinner("Processing... This avoids 403 errors using your secure cookies."):
                out_filename = "yt_download.mp4"
                
                ydl_save_opts = {
                    # Finds best combined video+audio file up to selected height
                    'format': f'best[height<={max_height}][ext=mp4]',
                    'outtmpl': out_filename,
                    'cookiefile': 'temp_cookies.txt' if os.path.exists("temp_cookies.txt") else None,
                    'quiet': True,
                    'no_warnings': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_save_opts) as ydl_s:
                    ydl_s.download([url])
                
                if os.path.exists(out_filename):
                    with open(out_filename, "rb") as f:
                        st.download_button(
                            label="💾 Save to Device",
                            data=f,
                            file_name=f"{title}.mp4",
                            mime="video/mp4"
                        )
                    # Clean up server storage
                    os.remove(out_filename)
                else:
                    st.error("Failed to generate file. Try a lower quality.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.info("Ensure your YOUTUBE_COOKIES are correctly set in Streamlit Secrets.")

# Cleanup temp file on script end if it exists
if os.path.exists("temp_cookies.txt"):
    try:
        os.remove("temp_cookies.txt")
    except:
        pass
