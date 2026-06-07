import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
import random

st.set_page_config(
    page_title="Word Cloud Generator",
    page_icon="☁️",
    layout="centered"
)

st.title("☁️ Personal Word Cloud Generator")

st.write("Paste text or upload a text file to generate a word cloud.")

text_input = st.text_area("Paste your text here", height=250)

uploaded_file = st.file_uploader(
    "Or upload a text file",
    type=["txt"]
)

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

st.subheader("Colour Options")

colour_mode = st.radio(
    "Choose colour mode",
    ["Built-in palette", "Custom 10-colour palette"]
)

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

selected_palette = "viridis"
custom_colours = []

if colour_mode == "Built-in palette":
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

    selected_palette = st.selectbox(
        "Select a palette",
        palette_options,
        index=0
    )

    st.markdown("### Selected Palette Preview")

    fig, ax = plt.subplots(figsize=(10, 0.8))
    ax.imshow(
        gradient,
        aspect="auto",
        cmap=plt.get_cmap(selected_palette)
    )
    ax.set_axis_off()
    st.pyplot(fig)

else:
    st.write("Pick up to 10 custom colours.")

    default_colours = [
        "#00AEEF",
        "#00FFB9",
        "#7A5CFF",
        "#FF5C8A",
        "#FFB000",
        "#2ECC71",
        "#E74C3C",
        "#34495E",
        "#F1C40F",
        "#9B59B6"
    ]

    colour_cols = st.columns(2)

    for i in range(10):
        with colour_cols[i % 2]:
            colour = st.color_picker(
                f"Colour {i + 1}",
                default_colours[i]
            )
            custom_colours.append(colour)

    st.markdown("### Custom Palette Preview")

    swatch_html = "<div style='display:flex; flex-wrap:wrap; gap:6px;'>"

    for colour in custom_colours:
        swatch_html += f"""
        <div style='
            width:50px;
            height:35px;
            background:{colour};
            border-radius:6px;
            border:1px solid #cccccc;
        '></div>
        """

    swatch_html += "</div>"

    st.markdown(swatch_html, unsafe_allow_html=True)

text = text_input

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")


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

    if colour_mode == "Custom 10-colour palette":

        def custom_colour_func(
            word,
            font_size,
            position,
            orientation,
            random_state=None,
            **kwargs
        ):
            return random.choice(custom_colours)

        wordcloud = WordCloud(
            width=width,
            height=height,
            background_color=background,
            stopwords=stopwords,
            max_words=max_words,
            collocations=False,
            color_func=custom_colour_func
        ).generate(text)

    else:
        wordcloud = WordCloud(
            width=width,
            height=height,
            background_color=background,
            stopwords=stopwords,
            max_words=max_words,
            colormap=selected_palette,
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