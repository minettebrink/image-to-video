# Guide to Deploy and Build an Image-to-Video Generator App

Here, you can find information about how to deploy the app and how it was built.

## Getting Started

Follow the steps below to deploy an Image-to-Video converter to your Koyeb account.

To use this repository, you need:
- A Koyeb account to build the Dockerfile and deploy to the platform. If you don't already have an account, you can sign up for free, link to [sign up](https://app.koyeb.com/auth/signup).
- Access to CPU and GPU Instances on Koyeb.


### Deploy the Application
Remember to deploy the backend first and then the frontend. If you use the Deploy to Koyeb buttons, you can link your service to your forked repository to push changes.

#### Frontend
[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?name=image-to-video-frontend&repository=minettebrink%2Fimage-to-video&branch=main&workdir=front_end&builder=dockerfile&dockerfile=.%2FDockerfile&instance_type=small&regions=par&env%5BVITE_BACKEND_URL%5D=https%3A%2F%2Fhelpful-cloe-challenge-0065b024.koyeb.app&ports=5173%3Bhttp%3B%2F&hc_protocol%5B5173%5D=tcp&hc_grace_period%5B5173%5D=5&hc_interval%5B5173%5D=30&hc_restart_limit%5B5173%5D=3&hc_timeout%5B5173%5D=5&hc_path%5B5173%5D=%2F&hc_method%5B5173%5D=get)

You'll need to configure the deployment source by adding the link to the repo you forked.

<img src="assets/configure_deployment_source.png" width="500" alt="Service Type">

To configure the builder, select Dockerfile and write `./Dockerfile` in the docker file location and in the Work directory `/front_end`. 
    
<img src="assets/builder_frontend.png" width="500" alt="Service Type">


#### Backend
[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?name=image-to-video-backend&repository=minettebrink%2Fimage-to-video&branch=main&workdir=%2Fback_end&builder=dockerfile&dockerfile=.%2FDockerfile&instance_type=gpu-nvidia-l40s&regions=eu&instances_min=0&autoscaling_sleep_idle_delay=300&env%5BALLOWED_ORIGINS%5D=https%3A%2F%2Fmale-othilia-challenge-af621831.koyeb.app&hc_grace_period%5B8000%5D=900&hc_interval%5B8000%5D=60&hc_timeout%5B8000%5D=60)

You'll need to configure the deployment source by adding the link to the repo you forked.

<img src="assets/configure_deployment_source.png" width="500" alt="Service Type">

To configure the builder, select Dockerfile and write `./Dockerfile` in the docker file location and the Work directory `/back_end`. 

<img src="assets/builder_backend.png" width="500" alt="Builder Backend">


Alternatively, you can manually create the application as described below.


When clicking Create Service on your Koyeb account, choose GitHub and add the link to your public GitHub repo. After selecting the instance, click the Create Web Service button.

<img src="assets/service_type.png" width="500" alt="Service Type">

Select GitHub as the deployment method.
Choose the repository containing your application code.


### For the frontend: 
- To configure the builder, select Dockerfile and write `./Dockerfile` in the docker file location and in the Work directory `/front_end`. 
    
    <img src="assets/builder_frontend.png" width="500" alt="Service Type">
- After the backend has started, add the URL as an environment variable with the name `VITE_BACKEND_URL`. 
    
    <img src="assets/variable_frontend.png" width="500" alt="Variable Frontend">
- In the Instance section, select the CPU category and choose Small. 
    
    <img src="assets/instance_frontend.png" width="500" alt="Instance Frontend">
- Add to Configure ports Port 5173 and Protocol HTTP. 
    
    <img src="assets/port_frontend.png" width="500" alt="Port Frontend">
- Click Deploy!
- The repository will be pulled, built, and deployed on Koyeb. Once the deployment is complete, it will be accessible using the Koyeb subdomain for your service 🚀

### For the backend: 
- To configure the builder, select Dockerfile and write `./Dockerfile` in the docker file location and the Work directory `/back_end`. 

    <img src="assets/builder_backend.png" width="500" alt="Builder Backend">
- After you've deployed the frontend, add the frontend URL as an environment variable with the name `ALLOWED_ORIGINS` to the backend. 
   
    <img src="assets/variable_backend.png" width="500" alt="Variable Backend">
- In the Instance section, select the GPU category and choose L40s. 
    
    <img src="assets/instance_backend.png" width="500" alt="Instance Backend">
- Add to Configure ports Port the port you chose and Protocol HTTP. 

    <img src="assets/port_backend.png" width="500" alt="Port Backend">
- In the Health checks section, set the Grace period to 900 seconds and Interval and Timeout to 60s. This will allow LTX-Video to download from Hugging Face and initialise the server. 

    <img src="assets/health_check_backend.png" width="500" alt="Health Check Backend">
- Click Deploy.
- The repository will be pulled, built, and deployed on Koyeb. And you're ready to go 🚀 

 

## Running locally 

Running the backend and frontend locally isn't necessary, but here's a small guide if you want to fork the repo, make changes, and play around with it. In the [Workflow](#workflow) section, you can find a more detailed description of how to build the app.

### Backend

Note that you'll need a GPU on your machine to run the model locally.

First pip install the [requirements](back_end/requirements.txt), preferably in a virtual environment:
```bash
pip install -r requirements.txt
```

I've also included a small Python script to download the correct model weights. When iterating locally, you don't need to run this before starting the backend server.
```python
from huggingface_hub import hf_hub_download
hf_hub_download(repo_id="Lightricks/LTX-Video", filename="ltx-video-2b-v0.9.1.safetensors", local_dir="/models")
```

To start the backend locally in dev mode, run:
```bash
fastapi dev main.py
```

If you're using docker, you can instead run and build it locally like so:
```bash
docker build -t my-image-name .
docker run -d -p <port>:<port> --name my-container-name my-image-name
```

### Frontend
The frontend is built with Svelte. To run the frontend locally, first install the dependencies:

```bash
pnpm install
```

And then run the server:
```bash
pnpm run dev
```

And the dockerized version:
```bash
docker build -t  my-image-name .
docker run -d -p 5173:5173 --name <app-name> 
```



## Workflow
In this section, you can find a more detailed description of how to build the app.

1. Set up the frontend with Svelte 
```
pnpx sv create myapp
```
Select `SvelteKit minimal`, `Yes, using TypeScript syntax`, no need to add anything to the project, and select `pnpm` as package manager.
```
cd myapp
pnpm install
pnpm run dev
```
2. Setup the backend in a separet directory, install FastApi,
```
pip install "fastapi[standard]"
```
and to run it locally.
```
fastapi dev main.py
```
3. Connect the backend with frontend.
4. Add parameters and a `.mp4` file as the backend output to simulate the pipeline without the model. Run both the backend and frontend locally to see that everything works as you want.
5. Dockerize the frontend and backend separately, then test that `docker build` and `docker run` work correctly.
6. Deployed frontend to Koyeb (follow these [instructions](#for-the-frontend)) and test that the frontend works as you want to.
7. Deployed backend to Koyeb (follow these [instructions](#for-the-backend)) and test that the back- and frontend work correctly.
8. Add the script that downloads the model weights to the backend 
```python
from huggingface_hub import hf_hub_download
hf_hub_download(repo_id="Lightricks/LTX-Video", filename="ltx-video-2b-v0.9.1.safetensors", local_dir="/models")
```
9. Deploy the backend on Koyeb and verify the model weights download correctly by checking the console.
10. Add the part to load the model:
```python
local_model_path = "/models/ltx-video-2b-v0.9.1.safetensors"
transformer = LTXVideoTransformer3DModel.from_single_file(
  local_model_path, torch_dtype=torch.bfloat16
)
vae = AutoencoderKLLTXVideo.from_single_file(local_model_path, torch_dtype=torch.bfloat16)
pipe = LTXImageToVideoPipeline.from_pretrained(
  "Lightricks/LTX-Video", transformer=transformer, vae=vae, torch_dtype=torch.bfloat16
)
pipe.to("cuda")
```
11. Verify that the model loads correctly on Koyeb by checking the console.
12. If the model loads successfully in the console, proceed to test the web app.

## Troubleshooting

Common issues and their solutions: 
* **Port Conflicts**: Ensure ports backend and 5173 (frontend) are available and public and that the frontend and backend URLs are correct
* **Two or more requests** : If there are two or more requests at the same time, the backend might fail. This is because, for both videos, the file name would be `output.mp4`. This is fine for demonstration purposes but needs to be corrected for production.

## Helpful links
* [LTX-Video](https://huggingface.co/Lightricks/LTX-Video)
* [Koyeb Documentation](https://www.koyeb.com/docs)
* [SvelteKit](https://kit.svelte.dev/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Docker](https://docs.docker.com/)
* Link to the [project demo](https://youtu.be/eZfTr2Mq9d8)