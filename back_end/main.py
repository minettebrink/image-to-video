from fastapi import FastAPI, HTTPException, Response
from typing import Optional
from pydantic import BaseModel
import torch
from diffusers import AutoencoderKLLTXVideo, LTXImageToVideoPipeline, LTXVideoTransformer3DModel
from diffusers.utils import export_to_video, load_image
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os


app = FastAPI()

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,https://*.koyeb.app"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


local_model_path = "/models/ltx-video-2b-v0.9.1.safetensors"
transformer = LTXVideoTransformer3DModel.from_single_file(
  local_model_path, torch_dtype=torch.bfloat16
)
vae = AutoencoderKLLTXVideo.from_single_file(local_model_path, torch_dtype=torch.bfloat16)
pipe = LTXImageToVideoPipeline.from_pretrained(
  "Lightricks/LTX-Video", transformer=transformer, vae=vae, torch_dtype=torch.bfloat16
)
pipe.to("cuda")

class VideoGenerationRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = None
    image_url: str
    num_inference_steps: Optional[int] = 50
    width: Optional[int] = 704
    height: Optional[int] = 448
    guidance_scale: Optional[float] = 3.0


@app.post("/generate-video")
async def generate_video(request: VideoGenerationRequest):
    try:
        
        image = load_image(request.image_url)
        
        pipeline_params = {
            "image": image,
            "prompt": request.prompt,
            "negative_prompt": request.negative_prompt,
            "num_inference_steps": request.num_inference_steps or 50,
            "guidance_scale": request.guidance_scale or 7.5,
            "width": request.width,
            "height": request.height,
            "num_frames": 161
        }

        video = pipe(
            image=pipeline_params["image"],
            prompt=pipeline_params["prompt"],
            negative_prompt=pipeline_params["negative_prompt"],
            width=pipeline_params["width"],
            height=pipeline_params["height"],
            num_frames=pipeline_params["num_frames"],
            num_inference_steps=pipeline_params["num_inference_steps"],
        ).frames[0]

        output_path = "output.mp4"
        export_to_video(video, output_path, fps=24)

        
        with open(output_path, "rb") as video_file:
            video_data = video_file.read()

        return Response(
            content=video_data,
            media_type="video/mp4"
        )
    

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    