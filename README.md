# 🚀 Hunyuan3D Serverless API

A high-quality 3D model generation API that converts images and text prompts into downloadable 3D GLB files using Hunyuan3D technology.

## ✨ Features

- **Image-to-3D**: Upload any image and get a high-quality 3D model
- **Text-to-3D**: Enter a text prompt and generate 3D models
- **High Quality**: Maximum quality settings with texture generation
- **Progress Tracking**: Real-time progress updates
- **Downloadable GLB**: Base64 encoded 3D files ready for download
- **RunPod Ready**: Optimized for RunPod serverless deployment

## 🎯 API Endpoints

### Image-to-3D Generation
```json
{
  "input": {
    "image": "base64_encoded_image_data"
  }
}
```

### Text-to-3D Generation
```json
{
  "input": {
    "prompt": "a beautiful dragon sitting on a mountain"
  }
}
```

## 📊 Performance

- **Shape Generation**: ~15 seconds
- **Texture Generation**: ~30-45 seconds
- **Total Time**: ~45-60 seconds
- **File Size**: 15-25MB GLB files
- **Quality**: Maximum (2048x2048 textures)

## 🛠️ Deployment

### RunPod Serverless Configuration

**Hardware Requirements:**
- GPU: RTX 4090 (24GB VRAM)
- RAM: 24GB
- Storage: 50GB
- Timeout: 300 seconds

**Environment Variables:**
```
LD_LIBRARY_PATH=/usr/local/lib/python3.12/dist-packages/torch/lib:$LD_LIBRARY_PATH
CUDA_VISIBLE_DEVICES=0
HF_HUB_ENABLE_HF_TRANSFER=0
```

### Quick Deploy

1. **Connect Repository**: Link this GitHub repo to RunPod
2. **Configure Endpoint**: Set RTX 4090 GPU, 24GB RAM
3. **Deploy**: RunPod will automatically build and deploy
4. **Test**: Use RunPod's built-in testing interface

## 📁 Repository Structure

```
├── runpod_api.py          # Main serverless API code
├── Dockerfile             # Container configuration
├── requirements.txt       # Python dependencies
├── package.json          # RunPod configuration
├── test_api.py           # Local testing script
├── DEPLOYMENT_GUIDE.md   # Complete deployment guide
└── README.md             # This file
```

## 🧪 Testing

Test the API locally before deployment:

```bash
python test_api.py
```

## 💰 Cost Estimation

- **RTX 4090**: ~$0.50-0.80/hour
- **Per Request**: ~$0.05
- **Cold Start**: ~$0.04
- **Generation**: ~$0.01

## 🔧 Technical Details

### Models Used
- **Shape Generation**: `tencent/Hunyuan3D-2mini`
- **Texture Generation**: `tencent/Hunyuan3D-2`
- **Text-to-Image**: `Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled`
- **Background Removal**: `rembg`

### Generation Process
1. **Image Processing**: Resize, background removal, color enhancement
2. **Shape Generation**: 50 inference steps, 380 octree resolution
3. **Texture Generation**: 2048x2048 texture mapping
4. **Export**: GLB format with materials and textures

## 📞 Support

- **RunPod Docs**: https://docs.runpod.io/
- **Hunyuan3D Repo**: https://github.com/Tencent/Hunyuan3D-2
- **Issues**: Create GitHub issues for bugs or feature requests

## 📄 License

This project uses Hunyuan3D which is licensed under the TENCENT HUNYUAN NON-COMMERCIAL LICENSE AGREEMENT.

---

**Ready for deployment!** 🚀 Connect this repository to RunPod and start generating amazing 3D models!
