from PIL import Image
import numpy as np
from colorsys import rgb_to_hsv, hsv_to_rgb
from tqdm import tqdm

def create_animation_strip(input_path, num_frames, hue_shift_max=1):
    """
    Create an animation strip by copying an image with progressive hue shifts
    Returns both the strip image and a list of individual frame images
    
    Parameters:
    input_path (str): Path to the input image
    num_frames (int): Number of frames to generate
    hue_shift_max (float): Maximum hue shift value (default: 1)
    
    Returns:
    tuple: (strip_image, frames) where strip_image is the combined strip and frames is a list of individual frames
    """
    # Open and verify image
    img = Image.open(input_path).convert('RGB')
    width, height = img.size
    
    # Create new image for the strip
    strip_width = width * num_frames
    new_image = Image.new('RGB', (strip_width, height))
    
    # List to store individual frames for GIF
    frames = []
    
    # Convert to numpy array
    img_array = np.array(img)
    
    # Create progress bar
    pbar = tqdm(range(num_frames), desc="Generating frames", unit="frame")
    
    for frame in pbar:
        # Calculate hue shift for this frame
        progress = frame / (num_frames - 1)
        hue_shift = hue_shift_max * np.sin(progress * np.pi)
        
        # Create copy of original image
        frame_array = img_array.copy()
        
        # Convert RGB to HSV
        hsv_image = np.zeros_like(frame_array, dtype=np.float32)
        
        # Normalize RGB values to 0-1 range
        rgb_norm = frame_array.astype(np.float32) / 255.0
        
        # Calculate HSV values
        max_rgb = np.max(rgb_norm, axis=2)
        min_rgb = np.min(rgb_norm, axis=2)
        diff = max_rgb - min_rgb
        
        # Value
        hsv_image[:,:,2] = max_rgb
        
        # Saturation - avoiding division by zero
        saturation = np.zeros_like(max_rgb)
        nonzero_mask = max_rgb > 0
        saturation[nonzero_mask] = diff[nonzero_mask] / max_rgb[nonzero_mask]
        hsv_image[:,:,1] = saturation
        
        # Hue
        hsv_image[:,:,0] = np.zeros_like(max_rgb)
        
        # Handle non-zero differences to avoid division by zero
        nonzero_diff = diff != 0
        
        # Red is maximum
        mask = (rgb_norm[:,:,0] == max_rgb) & nonzero_diff
        if np.any(mask):
            hsv_image[:,:,0][mask] = (60 * ((rgb_norm[:,:,1] - rgb_norm[:,:,2])[mask] / diff[mask] + 0) % 360)
        
        # Green is maximum
        mask = (rgb_norm[:,:,1] == max_rgb) & nonzero_diff
        if np.any(mask):
            hsv_image[:,:,0][mask] = (60 * ((rgb_norm[:,:,2] - rgb_norm[:,:,0])[mask] / diff[mask] + 2) % 360)
        
        # Blue is maximum
        mask = (rgb_norm[:,:,2] == max_rgb) & nonzero_diff
        if np.any(mask):
            hsv_image[:,:,0][mask] = (60 * ((rgb_norm[:,:,0] - rgb_norm[:,:,1])[mask] / diff[mask] + 4) % 360)
        
        # Normalize hue to 0-1
        hsv_image[:,:,0] = hsv_image[:,:,0] / 360.0
        
        # Apply hue shift
        hsv_image[:,:,0] = (hsv_image[:,:,0] + hue_shift) % 1.0
        
        # Convert back to RGB
        h = hsv_image[:,:,0] * 6.0
        c = hsv_image[:,:,2] * hsv_image[:,:,1]
        x = c * (1 - abs(h % 2 - 1))
        
        rgb_image = np.zeros_like(frame_array, dtype=np.float32)
        
        # Convert HSV to RGB based on hue section
        mask = (h < 1)
        rgb_image[mask] = np.dstack((c[mask], x[mask], np.zeros_like(c[mask])))
        mask = (1 <= h) & (h < 2)
        rgb_image[mask] = np.dstack((x[mask], c[mask], np.zeros_like(c[mask])))
        mask = (2 <= h) & (h < 3)
        rgb_image[mask] = np.dstack((np.zeros_like(c[mask]), c[mask], x[mask]))
        mask = (3 <= h) & (h < 4)
        rgb_image[mask] = np.dstack((np.zeros_like(c[mask]), x[mask], c[mask]))
        mask = (4 <= h) & (h < 5)
        rgb_image[mask] = np.dstack((x[mask], np.zeros_like(c[mask]), c[mask]))
        mask = (5 <= h)
        rgb_image[mask] = np.dstack((c[mask], np.zeros_like(c[mask]), x[mask]))
        
        m = hsv_image[:,:,2] - c
        rgb_image += m[:,:,np.newaxis]
        
        # Convert back to uint8
        frame_array = (rgb_image * 255).astype(np.uint8)
        
        # Convert back to PIL Image
        frame_image = Image.fromarray(frame_array)
        
        # Add to frames list for GIF
        frames.append(frame_image.copy())
        
        # Paste into strip
        new_image.paste(frame_image, (frame * width, 0))
        
        # Update progress bar description with current frame
        pbar.set_postfix({"Frame": f"{frame+1}/{num_frames}"})
    
    pbar.close()
    return new_image, frames

def main():
    # Example usage
    input_path = "input_image.png"  # Your input image of any size
    num_frames = 100  # Number of frames to generate
    output_strip = "animated_strip.png"
    output_gif = "animated.gif"
    
    try:
        print("Starting animation generation...")
        # Create strip and get frames
        strip_image, frames = create_animation_strip(input_path, num_frames)
        
        print("Saving strip image...")
        # Save strip
        strip_image.save(output_strip, quality=100)
        
        print("Creating GIF...")
        # Save GIF with progress bar
        all_frames = frames + frames[-2:0:-1]  # Exclude first and last frame from reverse to avoid duplicates
        
        print(f"Saving GIF with {len(all_frames)} total frames...")
        all_frames[0].save(
            output_gif,
            save_all=True,
            append_images=all_frames[1:],
            duration=100,  # Duration for each frame in milliseconds
            loop=0  # 0 means loop forever
        )
        
        print(f"Successfully created animation strip with {num_frames} frames")
        print(f"Strip saved to: {output_strip}")
        print(f"GIF saved to: {output_gif}")
    except Exception as e:
        print(f"Error creating animation: {e}")

if __name__ == "__main__":
    main()