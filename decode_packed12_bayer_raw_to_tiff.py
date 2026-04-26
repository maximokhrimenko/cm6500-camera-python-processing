#%% 1. Define Paths and Setup
import os
import numpy as np
import cv2
import tifffile
import matplotlib.pyplot as plt

# Define your input and output paths
raw_file = r"F:\Ortho_2022\22223a_Simpson2Norman_raw\CM6500_032\C01_20220811_183510_00024G2.raw"
out_dir = r"F:\Ortho_2022\22223a_Simpson2Norman_raw\test_output"
os.makedirs(out_dir, exist_ok=True)

# Hardware specifications for the Imperx/Optech camera
width = 6600
height = 4400
expected_size = 43560000

#%% 2. Read the Raw Binary File
print("Reading pure binary sensor data...")
raw_bytes = np.fromfile(raw_file, dtype=np.uint8)

if len(raw_bytes) != expected_size:
    print(f"Warning: File size ({len(raw_bytes)}) does not match expected ({expected_size})")
else:
    print("File size matches perfectly. Proceeding to unpack...")

#%% 3. Unpack "packed12" binary format
print("Unpacking 12-bit data...")
# Reshape the 1D byte array into chunks of 3 bytes
byte_triplets = raw_bytes.reshape(-1, 3).astype(np.uint16)

# Extract the three individual bytes
b0 = byte_triplets[:, 0]
b1 = byte_triplets[:, 1]
b2 = byte_triplets[:, 2]

# Bitwise shift to reconstruct two 12-bit pixels from every 3 bytes
pixel_0 = b0 | ((b1 & 0x0F) << 8)
pixel_1 = (b1 >> 4) | (b2 << 4)

# Combine back into a 1D array of 16-bit integers
unpacked_pixels = np.empty(width * height, dtype=np.uint16)
unpacked_pixels[0::2] = pixel_0
unpacked_pixels[1::2] = pixel_1

# Reshape into the actual 2D image dimensions
bayer_image_16bit = unpacked_pixels.reshape((height, width))
print("Unpacking complete.")

#%% 4. Demosaic to RGB (VNG Filter)
print("Preparing for VNG Demosaicing...")
# The VNG algorithm strictly requires 8-bit data. 
# We scale down from the 12-bit max (4095) to 8-bit (255).
bayer_image_8bit = (bayer_image_16bit / 4095.0 * 255.0).astype(np.uint8)

print("Demosaicing to RGB...")
# ---> CHANGE 'BG' TO GB, RG, OR GR HERE IF YOUR DIAGNOSTIC LOOKED BETTER <---
bayer_flag = cv2.COLOR_BayerBG2RGB_VNG 
rgb_image_8bit = cv2.cvtColor(bayer_image_8bit, bayer_flag).astype(np.float32)

#%% 5. Auto White Balance and Radiometric Stretch
print("Applying Auto White Balance...")
# Calculate the average intensity of each color channel
avg_r = np.mean(rgb_image_8bit[:, :, 0])
avg_g = np.mean(rgb_image_8bit[:, :, 1])
avg_b = np.mean(rgb_image_8bit[:, :, 2])

# Calculate the overall "gray" average
avg_gray = (avg_r + avg_g + avg_b) / 3.0

# Scale channels so the overall image averages out to neutral gray
rgb_image_8bit[:, :, 0] = np.clip(rgb_image_8bit[:, :, 0] * (avg_gray / avg_r), 0, 255)
rgb_image_8bit[:, :, 1] = np.clip(rgb_image_8bit[:, :, 1] * (avg_gray / avg_g), 0, 255)
rgb_image_8bit[:, :, 2] = np.clip(rgb_image_8bit[:, :, 2] * (avg_gray / avg_b), 0, 255)

print("Applying radiometric stretch (Gamma)...")
# Apply a slight gamma correction to lift the shadows
gamma = 1.2
rgb_balanced = np.clip(((rgb_image_8bit / 255.0) ** (1.0 / gamma)) * 255.0, 0, 255).astype(np.uint8)

#%% 6. Save and Display
out_tiff = os.path.join(out_dir, "Decoded_Python.tif")
print(f"Saving LZW compressed TIFF to: {out_tiff}")
# Use LZW compression to match your original Optech LMS file sizes
tifffile.imwrite(out_tiff, rgb_balanced, compression='lzw')
print("Processing complete!")

plt.figure(figsize=(10, 7))
plt.imshow(rgb_balanced)
plt.title("Python Decoded & Balanced TIFF")
plt.axis('off')
plt.show()