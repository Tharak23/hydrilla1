# 🚀 Hunyuan3D RunPod Serverless API Deployment Guide

## 📋 **DEPLOYMENT CHECKLIST**

### ✅ **What We Have Ready:**
- ✅ Quality 3D generation working (20MB+ GLB files)
- ✅ Shape generation: ~15 seconds
- ✅ Texture generation: ~30-45 seconds  
- ✅ Custom rasterizer compiled
- ✅ All dependencies installed
- ✅ API code written (`runpod_api.py`)
- ✅ Docker configuration (`Dockerfile`)
- ✅ Package configuration (`package.json`)

### 🎯 **API Features:**
- ✅ **Image-to-3D**: Upload image → Get 3D model
- ✅ **Text-to-3D**: Enter prompt → Get 3D model
- ✅ **Progress Tracking**: Real-time progress updates
- ✅ **Downloadable GLB**: Base64 encoded files
- ✅ **Error Handling**: Comprehensive error messages
- ✅ **File Size Limits**: 50MB max file size

## 🛠️ **DEPLOYMENT STEPS**

### **Step 1: Prepare RunPod Environment**
```bash
# 1. Go to RunPod Console
# 2. Create new Serverless Endpoint
# 3. Configure:
#    - GPU: RTX 4090 (24GB VRAM)
#    - Memory: 24GB RAM
#    - Container Disk: 50GB
#    - Timeout: 300 seconds (5 minutes)
#    - Cold Start: Enabled
```

### **Step 2: Upload Files**
```bash
# Upload these files to RunPod:
# - runpod_api.py (main API code)
# - Dockerfile (container configuration)
# - package.json (dependencies)
```

### **Step 3: Configure Environment Variables**
```bash
LD_LIBRARY_PATH=/usr/local/lib/python3.12/dist-packages/torch/lib:$LD_LIBRARY_PATH
CUDA_VISIBLE_DEVICES=0
HF_HUB_ENABLE_HF_TRANSFER=0
```

### **Step 4: Deploy**
```bash
# RunPod will automatically:
# 1. Build Docker container
# 2. Install dependencies
# 3. Download models (~25GB)
# 4. Start API server
```

## 📊 **RESOURCE REQUIREMENTS**

### **Hardware:**
- **GPU**: RTX 4090 (24GB VRAM) - Required
- **RAM**: 24GB - Required
- **Storage**: 50GB - Required
- **CPU**: 8+ cores recommended

### **Model Sizes:**
- **Shape Model**: ~2GB
- **Texture Model**: ~8GB  
- **Text2Image Model**: ~5GB
- **Background Removal**: ~500MB
- **Total**: ~25GB

### **Performance:**
- **Cold Start**: ~2-3 minutes (model loading)
- **Warm Start**: ~30-60 seconds
- **Generation Time**: ~45-60 seconds total
- **File Size**: 15-25MB GLB files

## 🌐 **API USAGE**

### **Image-to-3D Generation:**
```json
{
  "input": {
    "image": "base64_encoded_image_data"
  }
}
```

### **Text-to-3D Generation:**
```json
{
  "input": {
    "prompt": "a beautiful dragon sitting on a mountain"
  }
}
```

### **Response Format:**
```json
{
  "success": true,
  "filename": "model_image-to-3d_20251025_123456.glb",
  "file_data": "base64_encoded_glb_file",
  "file_size": 20485760,
  "generation_time": 45.2,
  "generation_type": "image-to-3d",
  "progress": [
    {"message": "Processing input image", "percent": 5},
    {"message": "Generating 3D shape...", "percent": 10},
    {"message": "3D shape generated", "percent": 50},
    {"message": "Generating texture...", "percent": 60},
    {"message": "Texture generated", "percent": 90},
    {"message": "Model saved", "percent": 100}
  ]
}
```

## 💰 **COST ESTIMATION**

### **RunPod Pricing (Approximate):**
- **RTX 4090**: ~$0.50-0.80/hour
- **Cold Start**: ~3 minutes = ~$0.04
- **Generation**: ~1 minute = ~$0.01
- **Total per request**: ~$0.05

### **Optimization Tips:**
- Enable **warm starts** to reduce cold start costs
- Use **request batching** for multiple generations
- Implement **caching** for repeated requests

## 🔧 **TROUBLESHOOTING**

### **Common Issues:**
1. **Out of Memory**: Reduce texture size or use smaller models
2. **Timeout**: Increase timeout or optimize generation
3. **Model Loading**: Check internet connection for model downloads
4. **Custom Rasterizer**: Ensure CUDA compilation succeeded

### **Monitoring:**
- Check RunPod logs for errors
- Monitor GPU memory usage
- Track generation times
- Monitor API response times

## 🚀 **NEXT STEPS**

1. **Test Locally**: Test API code before deployment
2. **Deploy to RunPod**: Upload files and configure
3. **Test Endpoints**: Verify both image and text generation
4. **Monitor Performance**: Track costs and response times
5. **Scale**: Add more endpoints if needed

## 📞 **SUPPORT**

- **RunPod Docs**: https://docs.runpod.io/
- **Hunyuan3D Repo**: https://github.com/Tencent/Hunyuan3D-2
- **API Testing**: Use RunPod's built-in testing interface
