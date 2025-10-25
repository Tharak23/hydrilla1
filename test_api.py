#!/usr/bin/env python3
"""
Test script for Hunyuan3D RunPod API
Tests both image-to-3D and text-to-3D generation locally
"""

import os
import time
import base64
from PIL import Image
import io

# Import our API functions
from runpod_api import generate_3d_model, load_models

def test_image_to_3d():
    """Test image-to-3D generation"""
    print("🧪 Testing Image-to-3D Generation")
    print("=" * 50)
    
    # Load a test image
    image_path = "/workspace/Hunyuan3D-2/assets/cap.png"
    if not os.path.exists(image_path):
        print(f"❌ Test image not found: {image_path}")
        return False
    
    # Read and encode image
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    # Test input
    input_data = {
        "image": image_data
    }
    
    # Progress tracking
    progress_log = []
    def progress_callback(message, percent):
        progress_log.append({"message": message, "percent": percent})
        print(f"📊 {percent}% - {message}")
    
    # Generate 3D model
    print("🔄 Starting image-to-3D generation...")
    start_time = time.time()
    
    result = generate_3d_model(input_data, progress_callback)
    
    total_time = time.time() - start_time
    
    # Check result
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return False
    
    print(f"✅ Success! Generation took {total_time:.2f} seconds")
    print(f"📄 Filename: {result['filename']}")
    print(f"📊 File Size: {result['file_size'] / (1024*1024):.2f} MB")
    print(f"🎯 Generation Type: {result['generation_type']}")
    
    return True

def test_text_to_3d():
    """Test text-to-3D generation"""
    print("\n🧪 Testing Text-to-3D Generation")
    print("=" * 50)
    
    # Test input
    input_data = {
        "prompt": "a beautiful dragon sitting on a mountain"
    }
    
    # Progress tracking
    progress_log = []
    def progress_callback(message, percent):
        progress_log.append({"message": message, "percent": percent})
        print(f"📊 {percent}% - {message}")
    
    # Generate 3D model
    print("🔄 Starting text-to-3D generation...")
    start_time = time.time()
    
    result = generate_3d_model(input_data, progress_callback)
    
    total_time = time.time() - start_time
    
    # Check result
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return False
    
    print(f"✅ Success! Generation took {total_time:.2f} seconds")
    print(f"📄 Filename: {result['filename']}")
    print(f"📊 File Size: {result['file_size'] / (1024*1024):.2f} MB")
    print(f"🎯 Generation Type: {result['generation_type']}")
    
    return True

def main():
    """Main test function"""
    print("🚀 Hunyuan3D API Local Testing")
    print("=" * 60)
    
    # Load models
    print("📦 Loading models...")
    try:
        load_models()
        print("✅ Models loaded successfully!")
    except Exception as e:
        print(f"❌ Failed to load models: {e}")
        return
    
    # Test image-to-3D
    success1 = test_image_to_3d()
    
    # Test text-to-3D
    success2 = test_text_to_3d()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 60)
    print(f"Image-to-3D: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"Text-to-3D: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1 and success2:
        print("\n🎉 All tests passed! API is ready for deployment.")
    else:
        print("\n⚠️  Some tests failed. Check errors above.")

if __name__ == "__main__":
    main()
