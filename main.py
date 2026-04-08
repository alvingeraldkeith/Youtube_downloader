import streamlit as st
import yt_dlp
import os

# Page Config
st.set_page_config(page_title="YouTube Downloader", page_icon="🎥")
st.title("YouTube Video Downloader 🎥")
st.write("Enter a YouTube link below to generate a download button.")

# Input Field
url = st.text_input("Paste YouTube URL here:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        # Step 1: Fetch Video Metadata
        ydl_info_opts = {'quiet': True, 'no_warnings': True}
        
        with yt_dlp.YoutubeDL(ydl_info_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video')
            thumbnail = info.get('thumbnail')
            
            st.success(f"Found: **{title}**")
            if thumbnail:
                st.image(thumbnail, width=400)

            # Step 2: Download Process
            if st.button("Generate Download Link"):
                with st.spinner("Processing video... this involves merging high-quality tracks."):
                    
                    out_filename = "yt_video_download.mp4"
                    
                    # Advanced options to bypass 403 Forbidden and merge HQ files
                    ydl_save_opts = {
                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                        'outtmpl': out_filename,
                        'quiet': True,
                        'no_warnings': True,
                        'impersonate': 'chrome', # Bypasses bot detection
                        'extractor_args': {
                            'youtube': {
                                'player_client': ['android', 'web'],
                                'player_skip': ['webpage', 'configs']
                            }
                        }
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_save_opts) as ydl_s:
                        ydl_s.download([url])
                    
                    # Step 3: Create the Download Button for the User
                    if os.path.exists(out_filename):
                        with open(out_filename, "rb") as file:
                            st.download_button(
                                label="💾 Save Video to Device",
                                data=file,
                                file_name=f"{title}.mp4",
                                mime="video/mp4"
                            )
                        # Remove the file from the server to save space
                        os.remove(out_filename)
                    else:
                        st.error("Processing failed. Please try a different video.")

    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Tip: If you see 'Forbidden', the server might be temporarily throttled. Try again in a minute.")
