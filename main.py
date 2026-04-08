import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Downloader", page_icon="🎥")
st.title("YouTube Video Downloader 🎥")

url = st.text_input("Paste YouTube URL here:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        # Options for fetching info
        ydl_opts = {'quiet': True}
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video')
            st.write(f"### Found: {title}")
            
            # Show thumbnail
            st.image(info.get('thumbnail'))

            # Setup download button
            if st.button("Download in Best Quality"):
                st.info("🔄 Processing... this may take a minute for large videos.")
                
                # Download options - merges best video + best audio
                out_filename = "downloaded_video.mp4"
                ydl_save_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'outtmpl': out_filename,
                }
                
                with yt_dlp.YoutubeDL(ydl_save_opts) as ydl_s:
                    ydl_s.download([url])
                
                # Provide the file to the user
                with open(out_filename, "rb") as file:
                    st.download_button(
                        label="💾 Save to Device",
                        data=file,
                        file_name=f"{title}.mp4",
                        mime="video/mp4"
                    )
                # Clean up the server file after download
                os.remove(out_filename)

    except Exception as e:
        st.error(f"Error: {e}")
