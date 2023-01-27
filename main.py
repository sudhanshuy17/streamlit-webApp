from pdf2image import convert_from_path
import streamlit as st
import pytesseract
from PIL import Image
import io
import os

st.set_page_config(page_title="OCR App", page_icon=":guardsman:", layout="wide")

def process_file(file, pages=None):
    _, file_extension = os.path.splitext(file.name)
    file_extension = file_extension.lower()
    if file_extension == ".pdf":
        # Use pdf2image to convert pdf to image
        pages = convert_from_path(file, 500)
        text = ""
        for page in pages:
            image = page
            image = image.crop((0, 0, image.width, image.height/pages))
            text += pytesseract.image_to_string(image)
        return text
    else:
        # Open the image and use pytesseract to extract the text
        file.seek(0)
        image = Image.open(file)
        if pages:
            image = image.crop((0, 0, image.width, image.height/pages))
            text = pytesseract.image_to_string(image)
        return text


def main():
    st.title("OCR App")
    st.markdown("Upload a PDF, image, or TIFF file to extract text using OCR.")

    uploaded_file = st.file_uploader(
        "Choose a file", type=["pdf", "jpg", "jpeg", "png", "tiff"])
    if uploaded_file is not None:
        pages = st.number_input(
            "Number of Pages", min_value=1, max_value=20, value=1)
        text = process_file(uploaded_file, pages)
        st.write("Here's what I found:")
        st.write(text)

if __name__ == "__main__":
    main()
