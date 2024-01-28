import os
from PIL import Image
import os


def convert_to_jpeg_and_clean(file_paths):
    jpeg_files = []

    for file_path in file_paths:
        # Check if the file is not a JPEG
        if not file_path.lower().endswith('.jpeg') and not file_path.lower().endswith('.jpg'):
            try:
                # Open the image file
                with Image.open(file_path) as img:
                    # Define the new filename
                    new_filename = os.path.splitext(file_path)[0] + '.jpeg'

                    # Convert and save the image as JPEG
                    rgb_im = img.convert('RGB')
                    rgb_im.save(new_filename, 'JPEG')

                    print(f"Converted '{file_path}' to '{new_filename}'")

                    # Add the new filename to the list of JPEG files
                    jpeg_files.append(new_filename)

                    # Delete the old file
                    os.remove(file_path)
                    print(f"Deleted old file: '{file_path}'")
            except Exception as e:
                print(f"Failed to convert '{file_path}'. Error: {e}")
        else:
            # If the file is already a JPEG and starts with 'screenshot', add it to the list
            jpeg_files.append(file_path)

    return jpeg_files


def get_screenshot_files(desktop_path):
    screenshot_files = []

    # List all files and folders on the desktop
    for item in os.listdir(desktop_path):
        # Construct full file path
        item_path = os.path.join(desktop_path, item)

        # Check if it is a file and starts with 'screenshot'
        if os.path.isfile(item_path) and item.lower().startswith('screenshot'):
            screenshot_files.append(item_path)

    return screenshot_files

# Replace this with the path to your desktop
desktop_path = "/Users/davidandreas/Desktop" 

screenshots = convert_to_jpeg_and_clean(get_screenshot_files(desktop_path))
print(screenshots)
