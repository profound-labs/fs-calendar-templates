#!/usr/bin/env python3

import sys
from PIL import Image

def multiply_effect(image_path, output_path, factor=1.3):
    with Image.open(image_path) as img:
        # Ensure the image is in RGB mode
        rgb_img = img.convert('RGB')

        width, height = rgb_img.size

        # Create a new image for the result
        result_img = Image.new('RGB', (width, height))

        # Iterate through each pixel and apply the multiply effect
        for x in range(width):
            for y in range(height):
                px = rgb_img.getpixel((x, y))
                if not isinstance(px, tuple):
                    print("Can't get the pixel value")
                    sys.exit(-1)

                r, g, b = px

                # Invert colors (treat white as 0)
                inv_r, inv_g, inv_b = 255 - r, 255 - g, 255 - b

                # Apply multiplication
                mult_r = int(min(inv_r * factor, 255))
                mult_g = int(min(inv_g * factor, 255))
                mult_b = int(min(inv_b * factor, 255))

                # Invert colors back
                res_r, res_g, res_b = 255 - mult_r, 255 - mult_g, 255 - mult_b

                result_img.putpixel((x, y), (res_r, res_g, res_b))

        result_img.save(output_path)

if __name__ == "__main__":
    multiply_effect(sys.argv[1], sys.argv[2], float(sys.argv[3]))
