# Hunyuan3D 2.0 - GCP Docker Setup

## Overview

This document describes how to build and run Hunyuan3D 2.0 on Google Cloud Platform using Docker. It provides instructions for building the Docker image, running the container, and using the provided example script `examples/textured_shape_gen.py` to generate textured 3D assets.

## Prerequisites

- A GCP VM with NVIDIA GPU and Docker installed.
- NVIDIA Container Toolkit configured for GPU support.
- Git installed.

## Build Docker Image

```bash
# Clone the repository and build the image
git clone https://github.com/Tencent-Hunyuan/Hunyuan3D-2.git
cd Hunyuan3D-2
docker build -t hunyuan3d:2.0-gcp -f Dockerfile .
```

---

## Run Container
```bash
# Run the container with mounted volumes for assets and outputs
docker run --gpus all --rm -it \
  -v $(pwd)/assets:/app/Hunyuan3D-2/assets \
  -v $(pwd)/outputs:/app/Hunyuan3D-2/outputs \
  hunyuan3d:2.0-gcp
```

---

## Using the Example Script
Inside the container, execute:
```bash
python examples/textured_shape_gen.py
```
This script will:
1. Remove the background from `assets/demo.png.`
2. Generate a 3D mesh using `Hunyuan3DDiTFlowMatchingPipeline.`
3. Apply texture using `Hunyuan3DPaintPipeline.`
4. Save outputs to `outputs/demo_mini.glb` and `outputs/demo_textured_mini.glb.`

---
## Directory Structure
```bash
Hunyuan3d_2_docker/
├── assets/                     # Sample images
├── outputs/                    # Generated meshes
├── examples/
│   └── textured_shape_gen.py   # Example usage script
├── Dockerfile                  # Dockerfile for GCP
├── package_versions.txt        # Package Versions Reference
└── README.md
```

### Package Versions
A separate file `package_versions.txt` contains the full list of installed packages and their versions for the `hunyuan_gpu` environment. This can be regenerated with:
```bash
pip freeze > package_versions.txt
```
Refer to package_versions.txt for full compatibility reference.
