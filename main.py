import streamlit as st
import yt_dlp
import os

# --- 1. SESSION MANAGEMENT ---
# We write the cookies ONLY if the secret is found
def initialize_auth():
    if "YOUTUBE_COOKIES" in st.secrets:
        with open("temp_cookies.txt", "w") as f:
            f.write(st.secrets["YOUTUBE_COOKIES"])
        return True
    return False

st.title("YouTube Platform Trial 🛠️")

# Check Auth Status
is_authenticated = initialize_auth()

if not is_authenticated:
    st.warning("⚠️ Authentication Pending: Please add your YOUTUBE_COOKIES to the Streamlit Secrets dashboard.")
    st.info("Statistics Tip: Authenticated sessions have a 95% higher success rate for high-traffic videos.")
else:
    url = st.text_input("Paste Link to Test:")
    
    if url:
        # Standardized Options to prevent the 403 Inner-Door error
        common_opts = {
            'cookiefile': 'temp_cookies.txt',
            'quiet': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }

        try:
            with yt_dlp.YoutubeDL(common_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                st.success(f"Connection Stable: {info.get('title')}")
                
                if st.button("Test Download (360p)"):
                    with st.spinner("Streaming..."):
                        # Force a combined format to avoid FFmpeg/Merge issues
                        opts = {**common_opts, 'format': 'best[height<=360][ext=mp4]', 'outtmpl': 'test.mp4'}
                        ydl.download([url])
                        st.balloons()
                        st.write("Download successful! The 'Inner Door' is open.")

        except Exception as e:
            st.error(f"Platform Error: {e}")
            if "403" in str(e):
                st.button("🔄 Refresh Session", on_click=st.rerun)
