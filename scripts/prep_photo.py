#!/usr/bin/env python3
"""Portrait photo preparation script.

Removes background, enhances contrast, crops, and resizes a portrait photo.
Usage: python scripts/prep_photo.py <input_image>
Output: source-prepped.png
"""

import os
import sys

import cv2
import numpy as np
from PIL import Image

try:
    from rembg import new_session, remove
except ImportError:
    print("rembg is not installed. Please install it using 'pip install rembg'.")
    sys.exit(1)


def process_image(input_path, output_path="source-prepped.png", max_height=800):
    try:
        # Load the image using PIL
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        with open(input_path, "rb") as f:
            input_bytes = f.read()

        print("Removing background...")
        # Initialize rembg session using u2net
        session = new_session("u2net")
        output_bytes = remove(input_bytes, session=session)
        import io

        img = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

        print("Enhancing contrast with CLAHE...")
        # Convert to cv2 format to apply CLAHE
        cv_img = np.array(img)
        # Extract RGB and Alpha
        bgr = cv2.cvtColor(cv_img[:, :, :3], cv2.COLOR_RGB2BGR)
        alpha = cv_img[:, :, 3]

        # Convert to LAB to enhance luminance
        lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        # Apply CLAHE to L-channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)

        limg = cv2.merge((cl, a, b))
        enhanced_bgr = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        enhanced_rgb = cv2.cvtColor(enhanced_bgr, cv2.COLOR_BGR2RGB)

        # Merge back with alpha
        enhanced_rgba = np.dstack((enhanced_rgb, alpha))
        img = Image.fromarray(enhanced_rgba, "RGBA")

        print("Cropping excessive empty space...")
        # Trim transparent borders
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)

        print(f"Resizing to max height of {max_height}px...")
        # Resize preserving aspect ratio
        width, height = img.size
        if height > max_height:
            new_width = int(width * (max_height / height))
            img = img.resize((new_width, max_height), Image.Resampling.LANCZOS)

        img.save(output_path)
        print(f"Success! Saved processed image to {output_path}")

    except Exception as e:
        print(f"Error processing image: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py <input_image>")
        sys.exit(1)

    input_file = sys.argv[1]
    # save to project root
    output_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "source-prepped.png",
    )
    process_image(input_file, output_file)
