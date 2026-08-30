#!/usr/bin/env python
# Quick camera test script

import cv2
import time

print("[*] Testing camera...")

for idx in range(3):
    print(f"\n[*] Testing camera index {idx}...")
    cap = cv2.VideoCapture(idx)
    
    if not cap.isOpened():
        print(f"  [!] Failed to open camera {idx}")
        continue
    
    print(f"  [+] Camera {idx} opened")
    
    # Try to read frames
    success_count = 0
    for i in range(10):
        ret, frame = cap.read()
        if ret and frame is not None:
            success_count += 1
            print(f"  [+] Frame {i}: OK (shape: {frame.shape})")
        else:
            print(f"  [!] Frame {i}: FAILED")
        time.sleep(0.1)
    
    cap.release()
    print(f"  [Summary] {success_count}/10 frames successful")
    
    if success_count > 0:
        print(f"\n[SUCCESS] Camera {idx} is working!")
        break
else:
    print("\n[FAILURE] No working camera found!")
    print("\nTroubleshooting:")
    print("1. Check if camera is plugged in")
    print("2. Check Device Manager for camera drivers")
    print("3. Try restarting the computer")
    print("4. Disable and re-enable camera in Device Manager")
