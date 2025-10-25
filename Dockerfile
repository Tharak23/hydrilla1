FROM runpod/pytorch:2.8.0-py3.12-cuda12.8.0-devel-ubuntu22.04

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
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install runpod torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
RUN pip install diffusers transformers accelerate safetensors
RUN pip install pillow numpy trimesh rembg
RUN pip install huggingface-hub

# Clone Hunyuan3D repository
RUN git clone https://github.com/Tencent/Hunyuan3D-2.git
WORKDIR /workspace/Hunyuan3D-2

# Install Hunyuan3D
RUN pip install -e .

# Compile custom rasterizer
WORKDIR /workspace/Hunyuan3D-2/hy3dgen/texgen/custom_rasterizer
RUN python setup.py build_ext --inplace
RUN python setup.py install

# Set environment variables
ENV LD_LIBRARY_PATH=/usr/local/lib/python3.12/dist-packages/torch/lib:$LD_LIBRARY_PATH
ENV CUDA_VISIBLE_DEVICES=0
ENV HF_HUB_ENABLE_HF_TRANSFER=0

# Create output directory
RUN mkdir -p /tmp/outputs

# Copy API files
WORKDIR /workspace
COPY runpod_api.py .
COPY package.json .

# Expose port (if needed for debugging)
EXPOSE 8000

# Set default command
CMD ["python", "runpod_api.py"]
