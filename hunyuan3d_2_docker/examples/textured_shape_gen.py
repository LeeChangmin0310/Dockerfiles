import time

import torch
from PIL import Image

from hy3dgen.rembg import BackgroundRemover
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
from hy3dgen.texgen import Hunyuan3DPaintPipeline

# Load and prepare image
image_path = 'assets/demo.png'
image = Image.open(image_path).convert("RGBA")  # Ensure image has alpha channel

# Remove background if image is RGB
if image.mode == 'RGB':
    rembg = BackgroundRemover()  # Initialize background remover
    image = rembg(image)         # Apply background removal

# Initialize shape generation pipeline
pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
    'tencent/Hunyuan3D-2mini',
    subfolder='hunyuan3d-dit-v2-mini',
    variant='fp16'
)

# Initialize texture generation pipeline
pipeline_texgen = Hunyuan3DPaintPipeline.from_pretrained('tencent/Hunyuan3D-2')  # Load texture model

# Generate shape
start_time = time.time()
mesh = pipeline(
    image=image,
    num_inference_steps=50,
    octree_resolution=380,
    num_chunks=20000,
    generator=torch.manual_seed(12345),
    output_type='trimesh'
)[0]
print(f"--- {time.time() - start_time} seconds ---")
mesh.export('outputs/demo_mini.glb')  # Save generated mesh

# Apply texture and save
# Texture the mesh\ nmesh_textured.export('outputs/demo_textured_mini.glb')  
mesh_textured = pipeline_texgen(mesh, image=image) # Save textured mesh
