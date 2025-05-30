# README

## Sample `.env` File

```env
OPEN_AI_KEY="sk-"
```

---

## 1, Docker Image Build Command

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





## 2. 🚀 Deploy the Project to Render (Free Cloud Platform)

### 🛠️ Step 1: Create a Clean Git Repository

If you're working within an existing Git repository and want to push your project to a a branch of a new GitHub repository which you need to create manually by using the git UI. This does **not** alter your existing working directory.

#### 1.1 Add a New Remote

Use the following command to add a new remote for your GitHub repo:

```bash
git remote add rag_app_origin https://github.com/Afrin-Sultana/Rag-App.git
````

This creates a reference to your GitHub repository with the nickname `rag_app_origin`. You can now push or pull code from this remote.

#### 1.2 Push Local Branch to GitHub

Now push your local branch (e.g., `RAG_with_ChromaDB`) to the `main` branch of the new repository:

```bash
git push rag_app_origin RAG_with_ChromaDB:main
```

This command takes the local branch `RAG_with_ChromaDB` and pushes it to the `main` branch on the `rag_app_origin` remote.

> 📌 **Note:** Make sure you run the above commands from the **root directory** of your local Git repository.

Example terminal session:

```bash
(.venv) afrinsultana@Afrins-Air RAG_with_Chroma % cd ..
(.venv) afrinsultana@Afrins-Air Git_Projects % cd RAG_with_Chroma 
(.venv) afrinsultana@Afrins-Air RAG_with_Chroma % cd End_to_End_GenAI_Usecase 
(.venv) afrinsultana@Afrins-Air End_to_End_GenAI_Usecase % git remote add rag_app_origin https://github.com/Afrin-Sultana/Rag-App.git
(.venv) afrinsultana@Afrins-Air End_to_End_GenAI_Usecase % git push rag_app_origin RAG_with_ChromaDB:main
```

---

### 🧹 Step 2: Clone the Clean Repository Locally

Once the code has been pushed, you may want to clone the newly created GitHub repository into a clean folder for further development.

#### To clone the repository:

1. Navigate to the **parent directory** where you'd like to clone the project.
2. Run the following command:

```bash
git clone https://github.com/Afrin-Sultana/Rag-App.git
```

This will create a new folder named `Rag-App/` containing your code and Git history.

You're now ready to continue development or deploy the project to Render!


