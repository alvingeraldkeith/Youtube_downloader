import streamlit as st
import yt_dlp
import os

# --- 1. CONFIG & AUTHENTICATION ---
st.set_page_config(page_title="Universal YT Downloader", page_icon="📺", layout="wide")

# This creates the physical cookie file YouTube needs
if "YOUTUBE_COOKIES" in st.secrets:
    with open("temp_cookies.txt", "w") as f:
        f.write(st.secrets["YOUTUBE_COOKIES"])

# --- 2. SIDEBAR (The Monetization & Branding Hub) ---
with st.sidebar:
    st.title("🚀 Platform Hub")
    st.write("Developed by **Ssekatawa Alvin Gerald**")
    st.divider()
    
    st.subheader("Support the Service")
    st.write("Help us maintain the server costs and keep the cookies fresh!")
    st.link_button("☕ Support via Mobile Money", "https://your-payment-link.com")
    
    st.divider()
    st.write("🎬 **Featured Content**")
    st.link_button("Visit Screen Tease YouTube", "https://youtube.com/@ScreenTease")
    
    st.info("💡 **Stats Tip:** Using a 360p resolution saves data and processes 3x faster on mobile networks.")

# --- 3. MAIN INTERFACE ---
st.title("YouTube Universal Downloader 🎥")
st.write("Enter a link below. We use secure session rolling to bypass 403 errors.")

url = st.text_input("Paste YouTube Link:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        # Configuration for metadata fetching
        ydl_opts_base = {
            'quiet': True,
            'no_warnings': True,
            'cookiefile': 'temp_cookies.txt' if os.path.exists("temp_cookies.txt") else None,
            # CRITICAL: Match this to the browser you used to export cookies
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts_base) as ydl:
            info = ydl.extract_info(url, download=False)
            st.success(f"Successfully Authenticated: **{info.get('title')}**")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(info.get('thumbnail'), use_container_width=True)
            with col2:
                option = st.selectbox("Choose Quality:", ["720p (High Quality)", "360p (Data Saver)"])
                height = "720" if "720p" in option else "360"
                
                if st.button("🚀 Prepare Download"):
                    with st.spinner("Streaming from YouTube via secure tunnel..."):
                        out_filename = "download.mp4"
                        
                        save_opts = {
                            **ydl_opts_base,
                            'format': f'best[height<={height}][ext=mp4]',
                            'outtmpl': out_filename,
                        }
                        
                        with yt_dlp.YoutubeDL(save_opts) as ydl_s:
                            ydl_s.download([url])
                        
                        if os.path.exists(out_filename):
                            with open(out_filename, "rb") as f:
                                st.download_button(
                                    label="💾 Download Now",
                                    data=f,
                                    file_name=f"{info.get('title')}.mp4",
                                    mime="video/mp4"
                                )
                            os.remove(out_filename)

    except Exception as e:
        st.error(f"Session Error: {e}")
        st.warning("If this continues, the cookies in 'Secrets' may have expired. Please refresh them.")

# Cleanup
if os.path.exists("temp_cookies.txt"):
    try: os.remove("temp_cookies.txt")
    except: pass
