from PIL import Image
import base64
from io import BytesIO

# Example base64 encoded image string (replace this with your actual base64 encoded image string)
base64_image_string = 'iVBORw0KGgoAAAANSUhEUgAAAQkAAAEJCAIAAAAICkUzAAEaHklEQVR42mS8d9xlZ1U2vNp9733OU2YmyUwmnSRIQgmEEEIwSFW6...'
Binary.createFromBase64('iVBORw0KGgoAAAANSUhEUgAAAQkAAAEJCAIAAAAICkUzAAEaHklEQVR42mS8d9xlZ1U2vNp9733OU2YmyUwmnSRIQgmEEEIwSFW6…', 0)

try:
    # Decode the base64 string to bytes
    image_bytes = base64.b64decode(base64_image_string)

    # Create a PIL Image object from the bytes
    image = Image.open(BytesIO(image_bytes))

    # Display the image
    image.show()

except Exception as e:
    print(f"Error: {e}")