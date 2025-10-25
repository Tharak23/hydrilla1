#!/usr/bin/env python3
"""
RunPod Serverless API for Hunyuan3D Generation
Handles both image-to-3D and prompt-to-3D generation
"""

import os
import time
import datetime
import json
import base64
import io
from pathlib import Path
from PIL import Image
import torch
import runpod

from hy3dgen.rembg import BackgroundRemover
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
from hy3dgen.texgen import Hunyuan3DPaintPipeline
from hy3dgen.text2image import HunyuanDiTPipeline

# =============================================================================
# 🎯 CONFIGURATION
# =============================================================================

# Model settings
SHAPE_MODEL = "tencent/Hunyuan3D-2mini"
TEXTURE_MODEL = "tencent/Hunyuan3D-2"
TEXT2IMAGE_MODEL = "Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled"

# Generation settings
INFERENCE_STEPS = 50
OCTREE_RESOLUTION = 380
NUM_CHUNKS = 20000
RANDOM_SEED = 12345

# Texture settings
TEXTURE_SIZE = 2048
RENDER_SIZE = 2048
BAKE_EXPONENT = 4

# Output settings
OUTPUT_FOLDER = "/tmp/outputs"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB limit

# =============================================================================
# 🚀 GLOBAL MODEL LOADING
# =============================================================================

# Global variables for model caching
shape_pipeline = None
texture_pipeline = None
text2image_pipeline = None
rembg_model = None

def load_models():
    """Load all models once at startup"""
    global shape_pipeline, texture_pipeline, text2image_pipeline, rembg_model
    
    print("🔄 Loading models for serverless API...")
    
    # Set environment for custom rasterizer
    os.environ['LD_LIBRARY_PATH'] = '/usr/local/lib/python3.12/dist-packages/torch/lib:' + os.environ.get('LD_LIBRARY_PATH', '')
    
    # Load shape generation model
    print("📦 Loading shape generation model...")
    shape_pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
        SHAPE_MODEL,
        subfolder='hunyuan3d-dit-v2-mini',
        variant='fp16'
    )
    print("✅ Shape model loaded")
    
    # Load texture generation model
    print("📦 Loading texture generation model...")
    texture_pipeline = Hunyuan3DPaintPipeline.from_pretrained(TEXTURE_MODEL)
    print("✅ Texture model loaded")
    
    # Load text-to-image model
    print("📦 Loading text-to-image model...")
    text2image_pipeline = HunyuanDiTPipeline(TEXT2IMAGE_MODEL)
    print("✅ Text-to-image model loaded")
    
    # Load background removal model
    print("📦 Loading background removal model...")
    rembg_model = BackgroundRemover()
    print("✅ Background removal model loaded")
    
    print("🎉 All models loaded successfully!")

# =============================================================================
# 🎨 IMAGE PROCESSING FUNCTIONS
# =============================================================================

def process_image(image_data, enhance_colors=True):
    """Process input image for 3D generation"""
    try:
        # Decode base64 image
        if isinstance(image_data, str):
            image_bytes = base64.b64decode(image_data)
        else:
            image_bytes = image_data
        
        # Load image
        image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
        
        # Resize if too large
        if max(image.size) > 2048:
            ratio = 2048 / max(image.size)
            new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Background removal
        if image.mode == 'RGB':
            image = rembg_model(image)
        
        # Color enhancement
        if enhance_colors:
            from PIL import ImageEnhance
            if image.mode == 'RGBA':
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background
            
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.2)
            
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.1)
            
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.1)
        
        return image, None
        
    except Exception as e:
        return None, f"Image processing error: {str(e)}"

def generate_text_to_image(prompt, seed=12345):
    """Generate image from text prompt"""
    try:
        image = text2image_pipeline(prompt, seed=seed)
        return image, None
    except Exception as e:
        return None, f"Text-to-image error: {str(e)}"

# =============================================================================
# 🎯 3D GENERATION FUNCTIONS
# =============================================================================

def generate_3d_shape(image, progress_callback=None):
    """Generate 3D shape from image"""
    try:
        if progress_callback:
            progress_callback("Generating 3D shape...", 10)
        
        mesh = shape_pipeline(
            image=image,
            num_inference_steps=INFERENCE_STEPS,
            octree_resolution=OCTREE_RESOLUTION,
            num_chunks=NUM_CHUNKS,
            generator=torch.manual_seed(RANDOM_SEED),
            output_type='trimesh'
        )[0]
        
        if progress_callback:
            progress_callback("3D shape generated", 50)
        
        return mesh, None
        
    except Exception as e:
        return None, f"Shape generation error: {str(e)}"

def generate_texture(mesh, image, progress_callback=None):
    """Generate texture for 3D model"""
    try:
        if progress_callback:
            progress_callback("Generating texture...", 60)
        
        textured_mesh = texture_pipeline(mesh, image=image)
        
        if progress_callback:
            progress_callback("Texture generated", 90)
        
        return textured_mesh, None
        
    except Exception as e:
        return None, f"Texture generation error: {str(e)}"

def save_model(mesh, filename, progress_callback=None):
    """Save 3D model to file"""
    try:
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        
        mesh.export(filepath)
        
        # Check file size
        file_size = os.path.getsize(filepath)
        if file_size > MAX_FILE_SIZE:
            os.remove(filepath)
            return None, f"File too large: {file_size / (1024*1024):.1f}MB (max: {MAX_FILE_SIZE / (1024*1024):.1f}MB)"
        
        if progress_callback:
            progress_callback("Model saved", 100)
        
        return filepath, None
        
    except Exception as e:
        return None, f"Save error: {str(e)}"

# =============================================================================
# 🚀 MAIN GENERATION FUNCTION
# =============================================================================

def generate_3d_model(input_data, progress_callback=None):
    """Main function to generate 3D model"""
    try:
        start_time = time.time()
        
        # Determine input type
        if 'prompt' in input_data:
            # Text-to-3D generation
            prompt = input_data['prompt']
            if progress_callback:
                progress_callback(f"Generating image from prompt: '{prompt}'", 5)
            
            image, error = generate_text_to_image(prompt)
            if error:
                return {"error": error}
            
            generation_type = "text-to-3d"
            
        elif 'image' in input_data:
            # Image-to-3D generation
            if progress_callback:
                progress_callback("Processing input image", 5)
            
            image, error = process_image(input_data['image'])
            if error:
                return {"error": error}
            
            generation_type = "image-to-3d"
            
        else:
            return {"error": "No prompt or image provided"}
        
        # Generate 3D shape
        mesh, error = generate_3d_shape(image, progress_callback)
        if error:
            return {"error": error}
        
        # Generate texture
        textured_mesh, error = generate_texture(mesh, image, progress_callback)
        if error:
            return {"error": error}
        
        # Save model
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"model_{generation_type}_{timestamp}.glb"
        
        filepath, error = save_model(textured_mesh, filename, progress_callback)
        if error:
            return {"error": error}
        
        # Read file as base64
        with open(filepath, 'rb') as f:
            file_data = base64.b64encode(f.read()).decode('utf-8')
        
        # Clean up
        os.remove(filepath)
        
        total_time = time.time() - start_time
        
        return {
            "success": True,
            "filename": filename,
            "file_data": file_data,
            "file_size": len(file_data),
            "generation_time": total_time,
            "generation_type": generation_type
        }
        
    except Exception as e:
        return {"error": f"Generation failed: {str(e)}"}

# =============================================================================
# 🌐 RUNPOD HANDLER
# =============================================================================

def handler(event):
    """RunPod serverless handler"""
    try:
        # Parse input
        input_data = event.get('input', {})
        
        # Validate input
        if not input_data:
            return {"error": "No input data provided"}
        
        # Check for required fields
        if 'prompt' not in input_data and 'image' not in input_data:
            return {"error": "Either 'prompt' or 'image' must be provided"}
        
        # Progress tracking
        progress_log = []
        def progress_callback(message, percent):
            progress_log.append({"message": message, "percent": percent})
        
        # Generate 3D model
        result = generate_3d_model(input_data, progress_callback)
        
        # Add progress log to result
        if "error" not in result:
            result["progress"] = progress_log
        
        return result
        
    except Exception as e:
        return {"error": f"Handler error: {str(e)}"}

# =============================================================================
# 🚀 STARTUP
# =============================================================================

if __name__ == "__main__":
    # Load models at startup
    load_models()
    
    # Start RunPod serverless
    runpod.serverless.start({"handler": handler})
