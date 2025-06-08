# -----------------------------------------------------------------------------
# See package_versions.txt and environment.yml for full dependency lists
# If you encounter version conflicts, refer to those files.
# -----------------------------------------------------------------------------

# 1. Base image with CUDA 11.8, cuDNN 8, and Ubuntu 20.04
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

# 2. Environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CONDA_DEFAULT_ENV=hunyuan_gpu
ENV CONDA_PREFIX=/opt/conda/envs/$CONDA_DEFAULT_ENV
ENV PATH=$CONDA_PREFIX/bin:/opt/conda/bin:$PATH

# 3. System dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      git wget build-essential python3-dev ca-certificates \
      libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# 4. Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda init bash

# 5. Create conda environment from environment.yml (alternative)
# RUN bash -lc "conda env create -f /app/Hunyuan3D-2/environment.yml && conda clean -afy"

# ─── OR ────────────────────────────────────────────────────────────────────────

# 5. Create and activate conda environment manually
RUN bash -lc "\
    conda create -n $CONDA_DEFAULT_ENV python=3.10 -y && \
    source activate $CONDA_DEFAULT_ENV && \
    conda install pytorch==2.3.1 torchvision==0.18.1 \
      torchaudio==2.3.1 pytorch-cuda=11.8 \
      -c nvidia -c pytorch -y && \
    conda clean -afy"

# 6. Use conda environment for subsequent RUN steps
SHELL ["conda", "run", "-n", "hunyuan_gpu", "/bin/bash", "-c"]

# 7. Clone repo and copy version-lock files
RUN git clone https://github.com/Tencent-Hunyuan/Hunyuan3D-2.git /app/Hunyuan3D-2
COPY package_versions.txt environment.yml /app/Hunyuan3D-2/
WORKDIR /app/Hunyuan3D-2

# 8. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -e .

# 9. Build and install custom rasterizer
RUN cd hy3dgen/texgen/custom_rasterizer && \
    pip install --no-cache-dir . && \
    cd /app/Hunyuan3D-2

# 10. Build and install differentiable renderer modules
RUN cd hy3dgen/texgen/differentiable_renderer && \
    if [ -f setup.py ]; then pip install --no-cache-dir .; fi && \
    cd /app/Hunyuan3D-2

# 11. Pin critical library versions for reproducibility
RUN pip install --no-cache-dir \
    transformers==4.48.0 \
    diffusers==0.33.1 \
    huggingface-hub==0.28.1 \
    numpy==2.0.1 \
    gradio==5.32.0

# 12. Default command: open a bash shell
CMD ["/bin/bash"]
