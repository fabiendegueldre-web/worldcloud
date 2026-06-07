import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

# ---------------------------
# Page Setup
# ---------------------------

st.set_page_config(
    page_title="Word Cloud Generator",
    page_icon="☁️",
    layout="centered"
)

st.title("☁️ Personal Word Cloud Generator")

st.write("Paste text or upload a text file to generate a word cloud.")

# ---------------------------
# Text Input
# ---------------------------

text_input = st.text_area(
    "Paste your text here",
    height=250
)

uploaded_file = st.file_uploader(
    "Or upload a text file",
    type=["txt"]
)

# ---------------------------
# Settings
# ---------------------------

st.subheader("Settings")

background = st.selectbox(
    "Background Colour",
    ["white", "black"]
)

custom_stopwords = st.text_input(
    "Additional words to exclude, comma separated",
    placeholder="example: company, meeting, people"
)

col1, col2 = st.columns(2)

with col1:
    width = st.slider("Image Width", 500, 2000, 1200)

with col2:
    height = st.slider("Image Height", 300, 1200, 700)

max_words = st.slider(
    "Maximum Number of Words",
    20,
    300,
    100
)

# ---------------------------
# Colour Palettes
# ---------------------------

st.subheader("Colour Palettes")

palette_options = [
    "viridis",
    "plasma",
    "inferno",
    "magma",
    "cividis",
    "Blues",
    "Greens",
    "Reds",
    "Purples",
    "cool",
    "hot",
    "tab10"
]

gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

st.write("Available palettes:")

for cmap in palette_options:
    st.caption(cmap)

    fig, ax = plt.subplots(figsize=(8, 0.4))
    ax.imshow(
        gradient,
        aspect="auto",
        cmap=plt.get_cmap(cmap)
    )
    ax.set_axis_off()
    st.pyplot(fig)

palette = st.selectbox(
    "Select a palette",
    palette_options,
    index=0
)

st.markdown("### Selected Palette Preview")

fig, ax = plt.subplots(figsize=(10, 0.8))
ax.imshow(
    gradient,
    aspect="auto",
    cmap=plt.get_cmap(palette)
)
ax.set_axis_off()
st.pyplot(fig)

# ---------------------------
# Get Text
# ---------------------------

text = text_input

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")

# ---------------------------
# Generate Word Cloud
# ---------------------------

if st.button("Generate Word Cloud"):

    if not text.strip():
        st.warning("Please enter some text or upload a file.")
        st.stop()

    stopwords = set(STOPWORDS)

    if custom_stopwords:
        extra_words = [
            word.strip().lower()
            for word in custom_stopwords.split(",")
        ]
        stopwords.update(extra_words)

    wordcloud = WordCloud(
        width=width,
        height=height,
        background_color=background,
        stopwords=stopwords,
        max_words=max_words,
        colormap=palette,
        collocations=False
    ).generate(text)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")

    st.pyplot(fig)

    img = wordcloud.to_image()
    buffer = BytesIO()
    img.save(buffer, format="PNG")

    st.download_button(
        label="📥 Download PNG",
        data=buffer.getvalue(),
        file_name="wordcloud.png",
        mime="image/png"
    )

    st.success("Word cloud generated successfully!")