import os
import argparse
from PIL import Image

def create_thumbnails(directory, suffix, width, height):
    """
    Create thumbnails of all image files in the specified directory.
    Thumbnails will be of specified width x height pixels and saved with the specified suffix.
    """
    # Define supported image formats
    supported_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif']
    
    # Count variables for summary
    total_images = 0
    successful_thumbnails = 0
    
    # Walk through the directory
    print(f"Scanning directory: {directory}")
    print(f"Creating thumbnails with dimensions: {width}x{height}")
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Check if it's a file and has a supported extension
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext in supported_formats:
                total_images += 1
                try:
                    # Open the image
                    with Image.open(file_path) as img:
                        # Create the thumbnail filename
                        base_name, extension = os.path.splitext(filename)
                        thumbnail_filename = f"{base_name}{suffix}{extension}"
                        thumbnail_path = os.path.join(directory, thumbnail_filename)
                        
                        # Skip if thumbnail already exists
                        if os.path.exists(thumbnail_path):
                            print(f"Skipping {filename} (thumbnail already exists)")
                            continue
                        
                        # Create the thumbnail
                        img_copy = img.copy()
                        img_copy.thumbnail((width, height), Image.Resampling.LANCZOS)
                        
                        # Create a new image with the exact dimensions
                        new_img = Image.new("RGBA" if img_copy.mode == 'RGBA' else "RGB", (width, height), (255, 255, 255))
                        
                        # Paste the thumbnail in the center of the new image
                        paste_x = (width - img_copy.width) // 2
                        paste_y = (height - img_copy.height) // 2
                        new_img.paste(img_copy, (paste_x, paste_y))
                        
                        # Save the thumbnail
                        new_img.save(thumbnail_path)
                        print(f"Created thumbnail for {filename}")
                        successful_thumbnails += 1
                        
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")
    
    # Print summary
    print(f"\nSummary:")
    print(f"Images found: {total_images}")
    print(f"Thumbnails created: {successful_thumbnails}")
    print(f"Thumbnails skipped or failed: {total_images - successful_thumbnails}")

def main():
    parser = argparse.ArgumentParser(description="Create thumbnails of images in a directory")
    parser.add_argument("directory", help="Directory containing images")
    parser.add_argument("--suffix", default="_thumb", help="Suffix to add to thumbnail filenames (default: _thumb)")
    parser.add_argument("--width", type=int, default=320, help="Width of thumbnails in pixels (default: 320)")
    parser.add_argument("--height", type=int, default=180, help="Height of thumbnails in pixels (default: 180)")
    
    args = parser.parse_args()
    
    # Verify the directory exists
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory.")
        return
    
    # Verify dimensions are positive
    if args.width <= 0 or args.height <= 0:
        print("Error: Width and height must be positive values.")
        return
    
    create_thumbnails(args.directory, args.suffix, args.width, args.height)

if __name__ == "__main__":
    main()