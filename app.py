import streamlit as st
import praw
import requests
from PIL import Image
import io

x = "test"


# Define Streamlit app interface
st.set_page_config(layout="wide")
st.title("Succession Meme Generator - Hosted on Hugging Spaces")
sidebar = st.sidebar

# Define inputs in sidebar
sidebar.title("Search Settings")
subreddit_name = sidebar.text_input("Enter a subreddit name", "successionTV")
limit = sidebar.number_input("Enter the limit of posts to search", min_value=1, max_value=100, value=20)

reddit = praw.Reddit(client_id='r9SFPvFBZddItqVEG121QQ',
                     client_secret='zZWvebRs3mc9qiXmONEEHXjlMYTZ2w',
                     user_agent='SuccessionMeme/1.0.0 (explore@datawithalex.com)')

subreddit = reddit.subreddit(subreddit_name)

search_query = st.text_input("Enter a search query", "Succession meme")
if st.button("Search"):
    images = []
    try:
        for submission in subreddit.search(search_query, limit=limit):
            if "jpg" in submission.url or "png" in submission.url:
                response = requests.get(submission.url)
                image = Image.open(io.BytesIO(response.content))
                image_width, image_height = image.size
                black_background = Image.new('RGB', (1080, 1920), color='black')
                x_offset = int((1080 - image_width) / 2)
                y_offset = int((1920 - image_height) / 2)
                black_background.paste(image, (x_offset, y_offset))
                images.append(black_background)

        if images:
            st.write(f"{len(images)} images found:")
            for i, image in enumerate(images):
                st.image(image, caption=f"Image {i+1}", width=800)
            if st.button("Download All Images"):
                for i, image in enumerate(images):
                    image.save(f"{search_query}_{i+1}.png")
                st.write("Images downloaded!")
        else:
            st.write("No image posts found.")
    except Exception as e:
        st.write(f"Error: {e}")
