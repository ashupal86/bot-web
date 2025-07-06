from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import docker

app = FastAPI()
docker_client = docker.from_env()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"], 
)


@app.get("/containers")
async def get_containers():
    containers= docker_client.containers.list(all=True)
    container_list = [{"id": container.id, "name": container.name,"status":container.status} for container in containers]
    return {"containers": container_list}

@app.get("/containers/{container_id}/start")
async def start_container(container_id: str):
    containers=docker_client.containers.get(container_id)
    containers.start();
    return {"status":f"{containers.name} container started"}

@app.get("/containers/{container_id}/stop")
async def stop_container(container_id: str):
    containers=docker_client.containers.get(container_id)
    containers.stop()
    return {"status": f"{containers.name} container stopped."}

@app.get("/containers/{container_id}/logs")
async def get_container_logs(container_id: str):
    containers=docker_client.containers.get(container_id)
    logs=containers.logs().decode("utf-8")
    return {"logs": logs}

@app.get("/")
async def root():
    return {"msg": "Welcome to the FastAPI based docker conatiner management system"}