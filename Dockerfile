FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    ninja-build \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install runpod
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install diffusers transformers accelerate safetensors
RUN pip install pillow "numpy<2.0" trimesh rembg onnxruntime
RUN pip install huggingface-hub

# Clone Hunyuan3D repository
RUN git clone https://github.com/Tencent/Hunyuan3D-2.git
WORKDIR /workspace/Hunyuan3D-2

# Install Hunyuan3D (skip custom rasterizer for now)
WORKDIR /workspace/Hunyuan3D-2
RUN pip install -e . --no-deps || pip install diffusers transformers accelerate

# Set CUDA environment variables
ENV TORCH_CUDA_ARCH_LIST="7.0;7.5;8.0;8.6;8.9;9.0"
ENV FORCE_CUDA=1

# Try to compile custom rasterizer (optional - will continue if it fails)
WORKDIR /workspace/Hunyuan3D-2/hy3dgen/texgen/custom_rasterizer
RUN python -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('CUDA arch:', torch.cuda.get_arch_list() if torch.cuda.is_available() else 'N/A')" || true
RUN python setup.py build_ext --inplace 2>&1 | tee build.log || true
RUN if [ -f build.log ]; then tail -20 build.log; fi
RUN echo "Custom rasterizer build attempted"

# Set environment variables
ENV LD_LIBRARY_PATH=/usr/local/lib/python3.10/dist-packages/torch/lib:$LD_LIBRARY_PATH
ENV CUDA_VISIBLE_DEVICES=0
ENV HF_HUB_ENABLE_HF_TRANSFER=0

# Create output directory
RUN mkdir -p /tmp/outputs

# Copy API files
WORKDIR /workspace
COPY handler.py .
COPY package.json .

# Expose port (if needed for debugging)
EXPOSE 8000

# Set default command
CMD ["python", "handler.py"]
