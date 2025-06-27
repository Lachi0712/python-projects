import os
import re
import requests
import wget
import streamlit as st

# Streamlit UI
st.set_page_config(page_title="Video Downloader", layout="centered")
st.title("📥 Facebook Video Downloader")
st.markdown("Paste your **Facebook video link**, and I'll help you download it!")

# Set up download directory
root = os.path.dirname(os.path.abspath(__file__))
download_path = os.path.join(root, "Downloads")
if not os.path.exists(download_path):
    os.mkdir(download_path)

# Input for link
link = st.text_input("🔗 Enter video link:")

if st.button("Download Video"):
    if not link:
        st.warning("🚨 Please enter a video link.")
    else:
        try:
            st.info("⏳ Fetching video info...")
            r = requests.get(link)

            if r.status_code == requests.codes.ok:
                try:
                    sd_match = re.search('sd_src:"(.+?)"', r.text)
                    hd_match = re.search('hd_src:"(.+?)"', r.text)

                    if not sd_match and not hd_match:
                        st.error("❌ Could not find any downloadable video in the link.")
                    else:
                        url = hd_match[1] if hd_match else sd_match[1]
                        st.success("🎥 Downloading... Please wait...")
                        filename = wget.download(url, out=download_path)
                        st.success(f"✅ Download complete: `{os.path.basename(filename)}`")
                        st.markdown(f"📁 Saved at: `{filename}`")
                except Exception as e:
                    st.error(f"Error during video extraction: {e}")
            else:
                st.error("❌ Invalid link or cannot be accessed.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
