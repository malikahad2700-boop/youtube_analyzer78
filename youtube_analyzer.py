from pytubefix import YouTube
import streamlit as st
import requests

st.title("Video Analyzer")

url = st.text_input("Enter your video URL")

if url:
    if url.strip() == "":
        st.error("Please enter a valid URL")
    else:
        try:
            yt = YouTube(url)

            choice = st.selectbox(
                "Choose one option",
                ["views", "description", "title", "thumbnail", "seo tags"]
            )

            if choice == "views":
                output = yt.views
                st.write("Views =", output)

            elif choice == "description":
                output = yt.description
                st.write("Description =", output)

            elif choice == "title":
                output = yt.title
                st.write("Title =", output)

            elif choice == "thumbnail":
                output = yt.thumbnail_url
                st.image(output, caption="Thumbnail")

            elif choice == "seo tags":
                words = (yt.description + " " + yt.title).lower().split()
                waste_been = {"is", "am", "are", "has", "have", "it", "was", "i", "-", "_", "(", ")", "the", "a", "an"}
                seo_tags = [word.strip(",.!?") for word in words if word not in waste_been]
                st.write("SEO Tags:", seo_tags)

            # ---------- Download Buttons ----------
            # Video download button
            if st.button("Download Video"):
                stream = yt.streams.get_highest_resolution()
                stream.download(filename="video.mp4")
                with open("video.mp4", "rb") as f:
                    st.download_button("Click here to save Video", f, file_name="video.mp4")

            # Thumbnail download button
            if st.button("Download Thumbnail"):
                response = requests.get(yt.thumbnail_url)
                with open("thumbnail.jpg", "wb") as f:
                    f.write(response.content)
                with open("thumbnail.jpg", "rb") as f:
                    st.download_button("Click here to save Thumbnail", f, file_name="thumbnail.jpg")

        except Exception as e:
            st.error(f"Error: {e}")
