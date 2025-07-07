from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import docker
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Docker client
client = docker.from_env()

# ENV Variables
API_KEY = os.getenv("API_KEY", "supersecret")
FRONTEND_IMAGE_URL = os.getenv("FRONTEND_IMAGE_URL", "ashu111/bot-web-frontend:latest")
BACKEND_IMAGE_URL = os.getenv("BACKEND_IMAGE_URL", "ashu111/bot-web-backend:latest")

app = FastAPI()

# CORS (you can restrict more in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


@app.post("/deployee")
async def deploye(x_api_key: str = Header(None)):
    # Validate API Key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        for container_name in ["bot-web-frontend", "bot-web-backend"]:
            try:
                old_container = client.containers.get(container_name)
                old_container.stop()
                old_container.remove()
                print(f" Removed old container: {container_name}")
            except docker.errors.NotFound:
                print(f"ℹNo existing container named {container_name}")


        # Pull latest image
        f_image = client.images.pull(FRONTEND_IMAGE_URL)
        b_image = client.images.pull(BACKEND_IMAGE_URL)
        print(f"Pulled latest frontend image: {f_image.tags}")
        print(f"Pulled latest backend image: {b_image.tags}")

        # Run new container
        container = client.containers.run(
            FRONTEND_IMAGE_URL,
            detach=True,
            name="bot-web-frontend",
            ports={"3000/tcp": 3000},  # Change as needed
            auto_remove=False,
        )
        print(f"Deployed new container: {container.name}")
        container_backend = client.containers.run(
            BACKEND_IMAGE_URL,
            detach=True,
            name="bot-web-backend",
            volumes={"/var/run/docker.sock": {"bind": "/var/run/docker.sock", "mode": "rw"}},
            ports={"8000/tcp": 8000},  # Change as needed
            auto_remove=False,
        )

        return {
            "status": "Container deployed successfully",
            "container_id": container.id,
            "image": [FRONTEND_IMAGE_URL, BACKEND_IMAGE_URL],
        }

    except docker.errors.APIError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


@app.get("/containers")
async def get_containers(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    containers = client.containers.list(all=True)
    return {
        "containers": [
            {"id": c.id, "name": c.name, "status": c.status, "image": c.image.tags}
            for c in containers
        ]
    }
