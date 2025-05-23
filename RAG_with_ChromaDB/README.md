# README

## Sample `.env` File

```env
OPEN_AI_KEY="sk-"
```

---

## Docker Image Build Command

### 1. Build the Docker Image

If you're in your current working directory (CWD) and your Dockerfile is inside a subfolder, use the following command to build the image from the correct location:

```bash
docker build -f <subfolder>/Dockerfile -t my-backend-image .
```

In our case, it would be:

```bash
docker build -f backend/Dockerfile -t my-backend-image .
```

---

### 2. Create a Docker Network

If you're going to use multiple services that share the same network, first create a network with the following command:

```bash
docker network create <network name>
```

---

### 3. Run the Docker Image Using the Custom Network

Run your Docker container attached to the custom network:

```bash
docker run -d -p 8000:8000 --name <container name> --network <network name> <image name>
```

In our case:

```bash
docker run -d -p 8000:8000 --name backend-container --network rag-network-manual my-backend-image
```

### 4. You can check the container status using the following command

```bash
docker ps
```

This will show the following info:
```bash
CONTAINER ID   IMAGE              PORTS                    NAMES
xxxxxxx        my-backend-image   0.0.0.0:8000->8000/tcp   backend-container

```

### 5. To check in which port your fast api is running or to get the URL

```bash
docker logs <container name>
```

### 6. To stop a container

```bash
docker stop <container name or container ID>
```


### 7. To remove a container

```bash
docker rm -f <container ID or name>
```



