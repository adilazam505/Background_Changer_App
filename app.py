import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance
import io

st.title("Background Changer & Image Enhancer App")

# Step 1: Upload original image
uploaded_image = st.file_uploader("Upload your original image", type=["jpg", "jpeg", "png"])

# Step 2: Upload new background
uploaded_bg = st.file_uploader("Upload background image", type=["jpg", "jpeg", "png"])

final_image = None  # To store result

# Step 3: Button to generate final image
if st.button("Generate Image"):
    if uploaded_image and uploaded_bg:
        # Open images
        original = Image.open(uploaded_image)
        new_bg = Image.open(uploaded_bg)

        # Remove background
        st.info("Removing background...")
        fg = remove(original)

        # Enhance foreground
        fg = ImageEnhance.Sharpness(fg).enhance(2.0)
        fg = ImageEnhance.Color(fg).enhance(1.5)

        # Resize background to match foreground
        new_bg = new_bg.resize(fg.size)

        # Merge foreground and background
        new_bg.paste(fg, (0, 0), fg)

        final_image = new_bg
        st.success("Image generated successfully!")
        st.image(final_image)
    else:
        st.warning("Please upload both images.")

# Step 4: Button to download image
if final_image:
    # Convert final image to bytes for download
    buf = io.BytesIO()
    final_image.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Download Final Image",
        data=byte_im,
        file_name="final_image.png",
        mime="image/png"
    )
