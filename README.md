# Image to Video Converter

A full-stack application that converts static images into videos using LTX-Video. The project consists of a SvelteKit frontend and a FastAPI backend service.

![Puppy Running](demos/demo.png)
## About the Project

This application allows users to upload images and convert them into videos using the LTX-Video model. The project is split into two main components:

- **Frontend**: Built with SvelteKit
- **Backend**: Using the LTX-Video model and FastAPI

## About LTX-Video Model

LTX-Video is a video generation model that generates image-to-video and text-to-video content. Image-to-video is used in this project.

### Model Capabilities
- Resolution: Works best with resolutions under 720 x 1280
- Frame Count: Supports up to 257 frames
- Input Requirements:
- Resolutions must be divisible by 32
- The number of frames must be divisible by 8 + 1 (e.g., 257)
### Limitations
- Video generation might not perfectly match prompts
- Quality depends heavily on prompting style



### Model Parameters
For this project, you can fill in the parameters except the number of frames, and we use the following parameters:

```python
{
    "width": 704,          
    "height": 480,         
    "guidance_scale": 7.5,
    "num_inference_steps": 50,  
    "num_frames": 161,
    "fps": 24,            
}
```
#### Additional Parameters
- **prompt**: Use English language prompts, and detailed, elaborate prompts work best.
- **negative_prompt**: what you don't want in your video.
- You can find more information about the parameters in the model [documentation](https://huggingface.co/docs/diffusers/main/en/api/pipelines/ltx_video#diffusers.LTXImageToVideoPipeline)


#### Input Image and Prompt
![start_image.png](demos/start_image.png)

- **Prompt:** A golden-brown puppy runs across a green lawn, its small paws kicking up grass as it moves. Its ears bounce with each stride. Its dark eyes are focused ahead. In the slightly blurred background, the expanse of the lawn stretches out, bordered by dense foliage.
- **Negative Prompt:** worst quality, inconsistent motion, blurry, jittery, distorted
- **Other Parameters:** Defeault

### Example Output
[![Watch the output on YouTube](https://youtu.be/GMcWAIBgbGY)](https://youtu.be/GMcWAIBgbGY)

## Getting Started

Follow the steps below to deploy an Image-to-Video converter to your Koyeb account.

## Requirements
To use this repository, you need:
- A Koyeb account to build the Dockerfile and deploy to the platform. If you don't already have an account, you can sign up for free.
- Access to GPU Instances on Koyeb.


### Running the Application
Remember first to deploy the frontend and then the backend 

#### Frontend
[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?name=image-to-video-frontend&repository=minettebrink%2Fimage-to-video&branch=main&workdir=front_end&builder=dockerfile&dockerfile=.%2FDockerfile&instance_type=small&regions=par&env%5BVITE_BACKEND_URL%5D=https%3A%2F%2Fhelpful-cloe-challenge-0065b024.koyeb.app&ports=5173%3Bhttp%3B%2F&hc_protocol%5B5173%5D=tcp&hc_grace_period%5B5173%5D=5&hc_interval%5B5173%5D=30&hc_restart_limit%5B5173%5D=3&hc_timeout%5B5173%5D=5&hc_path%5B5173%5D=%2F&hc_method%5B5173%5D=get)

#### Backend
[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?name=image-to-video-backend&repository=minettebrink%2Fimage-to-video&branch=main&workdir=%2Fback_end&builder=dockerfile&dockerfile=.%2FDockerfile&instance_type=gpu-nvidia-l40s&regions=eu&instances_min=0&autoscaling_sleep_idle_delay=300&env%5BALLOWED_ORIGINS%5D=https%3A%2F%2Fmale-othilia-challenge-af621831.koyeb.app&hc_grace_period%5B8000%5D=900&hc_interval%5B8000%5D=60&hc_timeout%5B8000%5D=60)

## Customize the project
If you want to customise and enhance this application, you will need to fork this repository.

### Backend
Run the [requirements file](back_end/requirements.txt) to download FastAPI. To run the backend locally, run 
```
fastapi dev main.py
```
To build and run the docker 
````
docker build -t my-image-name .
docker run -d -p <port>:<port> --name my-container-name my-image-name
````
### Frontend
The front end is built with Svelte. To run the frontend locally, use this command:
```
pnpm run dev
```
And to dockerised it:
```
docker build -t  my-image-name .
```
```
docker run -d -p 5173:5173 --name <app-name> -v $(pwd):/app svelte-app
```

### Deploy on Koyeb
If you use the Deploy to Koyeb button, you can link your service to your forked repository to be able to push changes. Alternatively, you can manually create the application as described below.

On the Koyeb Control Panel, on the Overview tab, click the Create Web Service button to begin.

Select GitHub as the deployment method.
Choose the repository containing your application code.

#### For the frontend: 
- To configure the builder, select Dockerfile and put ./Dockerfile in the docker file location and in the Work directory /front_end.
- After you get the backend, add the URL as an environmental variable with the name VITE_BACKEND_URL.
- In the Instance section, select the CPU category and choose Small.
- Add to Configure ports Port 5173 and Protocol HTTP.
- Click Deploy.
- The repository will be pulled, built, and deployed on Koyeb. Once the deployment is complete, it will be accessible using the Koyeb subdomain for your service.

#### For the backend: 
- To configure the builder, select Dockerfile and put ./Dockerfile in the docker file location and the Work directory /back_end.
- After you deploy the front end, add the URL as an environmental variable with the name ALLOWED_ORIGINS.
- In the Instance section, select the GPU category and choose L40s.
- Add to Configure ports Port the port you chose and Protocol HTTP.
- In the Health checks section, set the Grace period to 900 seconds and Interval and Timeout to 60s. This will allow LTX-Video to download from Hugging Face and initialise the server.
- Click Deploy.
- The repository will be pulled, built, and deployed on Koyeb. Once the deployment is complete, it will be accessible using the Koyeb subdomain for your service.

 



## Troubleshooting

Common issues and their solutions: 
* **Port Conflicts**: Ensure ports backend and 5173 (frontend) are available and that the frontend and backend URLs are correct



## Helpful links
* [LTX-Video](https://huggingface.co/Lightricks/LTX-Video)
* [Koyeb Documentation](https://www.koyeb.com/docs)
* [SvelteKit](https://kit.svelte.dev/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Docker](https://www.docker.com/)