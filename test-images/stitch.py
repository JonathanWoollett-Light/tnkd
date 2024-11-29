import cv2
import numpy as np
import glob

def stitch_images(image_paths):
    # Read images
    images = [cv2.imread(path) for path in image_paths]
    
    # Create a Stitcher object
    stitcher = cv2.Stitcher.create()
    
    # Perform stitching
    status, result = stitcher.stitch(images)
    
    if status == cv2.Stitcher_OK:
        return result
    else:
        print("Stitching failed!")
        return None

def main():
    # Get all image files in the current directory
    image_paths = glob.glob("*.png") + glob.glob("*.jpg") + glob.glob("*.jpeg")
    
    if len(image_paths) < 2:
        print("Not enough images found. Please ensure at least 2 images are in the directory.")
        return
    
    # Sort image paths to ensure consistent ordering
    image_paths.sort()
    
    # Perform stitching
    result = stitch_images(image_paths)
    
    if result is not None:
        # Save the result
        cv2.imwrite("stitched_result.jpg", result)
        print("Stitching completed. Result saved as 'stitched_result.jpg'")
    
if __name__ == "__main__":
    main()