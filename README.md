# 🐳 Text & Image → 3D — Docker Collection

GPU-ready Docker environments for state-of-the-art 3D generation / reconstruction:

| Folder                  | Model                 | Task                                | CUDA | Framework           |
| ----------------------- | --------------------- | ----------------------------------- | ---- | ------------------- |
| `worldgen_docker/`      | WorldGen + FLUX.1-dev | Text → 3D Mesh (.ply)               | 12.1 | PyTorch cu128       |
| `flash3d_docker/`       | Flash3D               | Single image → 3D Scene             | 11.8 | PyTorch 2.2.2       |
| `dreamscene360_docker/` | DreamScene360         | Text → 3D Scene (multi-view + .ply) | 12.4 | PyTorch 2.4.0 cu124 |
| `dreamscene_docker/`    | dreamscene            | Text → 3D Mesh (.ply)               | 11.8 | PyTorch cu118       |
| `hunyuan3d_2_docker/`   | Hunyuan3D 2.0         | Image/Text → Textured 3D (.glb/.ply) | 11.8 | PyTorch cu118       |

---

## ⚡ Quick Tour

```bash
git clone --recurse-submodules https://github.com/<your-repo>.git
cd <your-repo>

# ----------------------------------------------------
# WorldGen demo
cd worldgen_docker
docker build -t worldgen .
docker run --gpus all --rm -v $(pwd)/output:/app/WorldGen/output worldgen
cd ..

# ----------------------------------------------------
# Flash3D demo
cd flash3d_docker
docker build -t flash3d .
docker run --gpus all -it \
  -v $(pwd)/data:/workspace/flash3d/data \
  -v $(pwd)/output:/workspace/output \
  --name flash3d_container flash3d_autorun
cd ..

# ----------------------------------------------------
# DreamScene360 demo
cd dreamscene360_docker
docker build -t dreamscene360:cu124 .
docker run --gpus all -it --rm \
  -v $(pwd)/DreamScene360:/workspace/DreamScene360 \
  -v $(pwd)/pretrained:/workspace/DreamScene360/pre_checkpoints \
  dreamscene360:cu124

# Once inside the container, follow the instructions in:
#   /workspace/DreamScene360/README.md

# ----------------------------------------------------
# DreamScene demo
cd dreamscene_docker

# Build the Docker image (CUDA 11.8 + cuDNN)
docker build -t dreamscene:cu118 .

# Run the container with GPU and mount output directory
docker run --gpus all -it --rm \
  -v $(pwd)/DreamScene:/workspace/DreamScene \
  -v $(pwd)/output:/workspace/output \
  dreamscene:cu118

# Once inside the container:
# 1. Navigate to DreamScene directory
# 2. Run training using your config:
#    CUDA_VISIBLE_DEVICES=0 python main.py --object --config configs/objects/sample.yaml

# ----------------------------------------------------
# Hunyuan3D 2.0 demo
cd hunyuan3d_2_docker
docker build -t hunyuan3d2:cu118 .

# run container, mount assets/ and output/ for inputs & results
docker run --gpus all -it --rm \
  -v $(pwd)/assets:/app/Hunyuan3D-2/assets \
  -v $(pwd)/output:/app/Hunyuan3D-2/output \
  hunyuan3d2:cu118

# Once inside:
#   1) Refer to package_versions.txt & environment.yml for dependency versions
#   2) python examples/textured_shape_gen.py
cd ..
# ----------------------------------------------------

```

---

## ➕ Add a New Model

1. Create `<model>_docker/` with `Dockerfile`, scripts, `output/`.
2. Write `<model>_docker/README.md`.
3. Add the folder to the table above.
4. Follow this CLI pattern:

```bash
docker run --gpus all <image> <entrypoint> --input ... --out output/<name>
```

---

<!--## License

Each sub-folder inherits its upstream license. This meta-repo is MIT-licensed.-->
