import streamlit as st
import os

def save_uploadedfile(uploadedfile):
    with open(os.path.join("webui",uploadedfile.name),"wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File: " + uploadedfile.name + " to webui folder")

st.set_page_config(page_title="Pose Detection", layout="wide")

st.subheader("Upload Image Test")

uploaded_files = st.file_uploader("Choose an image file", accept_multiple_files=True, type=['png', 'jpg', 'mov', 'mp4'])
for uploaded_file in uploaded_files:
    if(uploaded_file.type[0:3] == "vid"):
        video_bytes = uploaded_file.read()
        st.video(video_bytes)
    else:
        image_bytes = uploaded_file.read()
        st.image(image_bytes)
    save_uploadedfile(uploaded_file)