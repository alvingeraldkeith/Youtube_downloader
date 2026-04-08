import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Simple YT Downloader", page_icon="📺")
st.title("YouTube Downloader (Stable Version) 📺")
st.write("This version uses 'Combined Formats' for better reliability.")

url = st.text_input("Paste YouTube Link:")

if url:
    try:
        # Step 1: Show video preview
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            st.info(f"Ready to download: **{info.get('title')}**")
            st.image(info.get('thumbnail'), width=300)

        # Step 2: Quality Selection
        # We limit to 720p and 360p because these often come as single files
        option = st.selectbox("Select Quality:", ["720p (High)", "360p (Small File)"])
        height = "720" if "720p" in option else "360"

        if st.button("Download Now"):
            with st.spinner("Fetching video..."):
                out_filename = "youtube_video.mp4"
                
                # The "Magic" Format: finds the best SINGLE file (video+audio) 
                # that is not taller than the selected height.
                ydl_opts = {
                    'format': f'best[height<={height}][ext=mp4]',
                    'outtmpl': out_filename,
                    'quiet': True,
                    'no_warnings': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl_s:
                    ydl_s.download([url])
                
                if os.path.exists(out_filename):
                    with open(out_filename, "rb") as f:
                        st.download_button(
                            label="💾 Save to Device",
                            data=f,
                            file_name=f"{info.get('title')}.mp4",
                            mime="video/mp4"
                        )
                    os.remove(out_filename)
                else:
                    st.error("Format not available. Try 360p.")

    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Tip: Some videos are restricted. Try a different link.")
