import streamlit as st
from PIL import Image, ImageOps
import io
import numpy as np
import imageio.v2 as imageio

st.set_page_config(page_title="Photo Dance Video Maker", page_icon="🎵")

st.title("🎵 Photo Dance Video Maker")
st.write("Photo upload karo, movement effect select karo aur short video banao.")

photo = st.file_uploader("1. Photo upload karo", type=["jpg", "jpeg", "png"])
audio = st.file_uploader("2. Optional: apni audio file upload karo", type=["mp3", "wav", "m4a"])

effect = st.selectbox("3. Dance/Movement effect", ["Zoom In", "Zoom Out", "Left to Right", "Right to Left"])
duration = st.slider("4. Video duration (seconds)", 5, 30, 10)
fps = 20

if photo:
    img = Image.open(photo).convert("RGB")
    st.image(img, caption="Your photo", use_container_width=True)

    if st.button("🎬 Create Video"):
        w, h = img.size
        frames = []

        for i in range(duration * fps):
            t = i / max(1, duration * fps - 1)

            if effect == "Zoom In":
                scale = 1.0 + 0.12 * t
                nw, nh = int(w * scale), int(h * scale)
                frame = img.resize((nw, nh), Image.Resampling.LANCZOS)
                frame = ImageOps.fit(frame, (w, h), method=Image.Resampling.LANCZOS)
            elif effect == "Zoom Out":
                scale = 1.12 - 0.12 * t
                nw, nh = int(w * scale), int(h * scale)
                frame = ImageOps.fit(img, (nw, nh), method=Image.Resampling.LANCZOS)
                canvas = Image.new("RGB", (w, h), "black")
                canvas.paste(frame, ((w-nw)//2, (h-nh)//2))
                frame = canvas
            else:
                shift = int((w * 0.10) * t)
                canvas = Image.new("RGB", (w, h), "black")
                crop = img.crop((0, 0, w, h))
                if effect == "Left to Right":
                    x = min(shift, w//10)
                else:
                    x = max(-shift, -w//10)
                frame = ImageOps.fit(img, (w, h), method=Image.Resampling.LANCZOS)

            frames.append(np.array(frame))

        out = io.BytesIO()
        imageio.mimsave(out, frames, format="mp4", fps=fps, codec="libx264")
        video_bytes = out.getvalue()

        st.success("Video ready! 🎉")
        st.video(video_bytes)

        st.download_button(
            "⬇️ Download Video",
            data=video_bytes,
            file_name="dance_video.mp4",
            mime="video/mp4"
        )

        if audio:
            st.info("Audio file upload ho gayi hai. Is version mein audio ko video ke saath merge karne ke liye FFmpeg/Pydub add karna hoga.")
else:
    st.info("Pehle apni photo upload karo.")
