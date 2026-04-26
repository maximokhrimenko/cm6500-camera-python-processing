# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 15:27:39 2026

@author: maxim.okhrimenko
"""

import os
import cv2
import numpy as np
import glob

# 1. Setup Paths
input_folder = r"F:\Ortho_2022\22223a_Simpson2Norman_raw\images"
output_folder = r"F:\Ortho_2022\22223a_Simpson2Norman_raw\images_python_balanced_v2"
os.makedirs(output_folder, exist_ok=True)

image_files = glob.glob(os.path.join(input_folder, "*.jpg"))
print(f"Processing {len(image_files)} images for TPhoto Test...")

def professional_balance(img):
    img = img.astype(np.float32)
    
    # A. Neutralize White Balance (Gray World)
    avg_b, avg_g, avg_r = np.mean(img[:,:,0]), np.mean(img[:,:,1]), np.mean(img[:,:,2])
    avg_gray = (avg_b + avg_g + avg_r) / 3.0
    img[:,:,0] *= (avg_gray / avg_b)
    img[:,:,1] *= (avg_gray / avg_g)
    img[:,:,2] *= (avg_gray / avg_r)
    
    # B. Reduce 'Vivid' Saturation (0.8 = 20% reduction)
    hsv = cv2.cvtColor(img.clip(0,255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:,:,1] *= 0.80 
    img = cv2.cvtColor(hsv.clip(0,255).astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
    
    # C. Gamma & Linear Stretch (Shadow Lift)
    # This lifts shadows (gamma 1.3) and ensures we don't 'blow out' highlights
    gamma = 1.3
    img = np.clip(((img / 255.0) ** (1.0 / gamma)) * 245.0, 0, 255) # Cap at 245 for safety
    
    return img.astype(np.uint8)

for file_path in image_files:
    img = cv2.imread(file_path)
    if img is None: continue
    balanced = professional_balance(img)
    cv2.imwrite(os.path.join(output_folder, os.path.basename(file_path)), balanced, [int(cv2.IMWRITE_JPEG_QUALITY), 98])

print("Batch complete. Ready for TerraPhoto.")