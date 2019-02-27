I#AUTHOR IS NOT ME "WASP"
# UNNOUN AUTHOR?
from PIL import Image
 
def resize_image(input_image_path,
                 output_image_path,
                 size):
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(size)
    resized_image.save(output_image_path)
 
