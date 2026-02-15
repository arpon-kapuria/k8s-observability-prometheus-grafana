# **Observability with Prometheus-Grafana**  
A complete guide on deploying a FastAPI application on Minikube, setting up Prometheus for metrics collection, and visualizing data on Grafana. The goal is to build a clean local observability pipeline.

📘 For detailed instructions, refer to this guide: [Project-Flow](./project-flow.md)

<br>

<p align="center">
   <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/Python-white?logo=python" alt="Python" />
   </a>
   <a href="https://uv.sh/">
      <img src="https://img.shields.io/badge/UV-white?logo=uv" alt="uv" />
   </a>
   <a href="https://fastapi.tiangolo.com/">
      <img src="https://img.shields.io/badge/FastAPI-white?logo=fastapi" alt="FastAPI" />
   </a>
   <a href="https://www.docker.com/">
      <img src="https://img.shields.io/badge/Docker-white?logo=docker" alt="Docker" />
   </a>
   <a href="https://kubernetes.io/">
      <img src="https://img.shields.io/badge/Kubernetes-white?logo=kubernetes" alt="Kubernetes" />
   </a>
   <a href="https://prometheus.io/">
      <img src="https://img.shields.io/badge/Prometheus-white?logo=prometheus" alt="Prometheus" />
   </a>
   <a href="https://grafana.com/">
      <img src="https://img.shields.io/badge/Grafana-white?logo=grafana" alt="Grafana" />
   </a>
   <a href="https://opensource.org/licenses/MIT">
      <img src="https://img.shields.io/badge/License-MIT-informational" alt="License" />
   </a>
</p>


---

## 📂 Project Structure

```text
k8s-observability-prometheus-grafana/
│
├─ k8s/
│   ├─ deployment.yaml    # Kubernetes Deployment (pods, replicas, image, resources)
│   └─ service.yaml       # Kubernetes Service (exposes pods inside/outside cluster) 
│
├─ src/
│   └─ app.py             # FastAPI application entry point
│
├─ pyproject.toml         # Dependency declaration (uv-managed)
├─ .python-version        # Python version used in this project (environment)
├─ uv.lock                # Locked dependencies for reproducibility
├─ Dockerfile             # Docker container configuration
├─ project-flow.md        # Step-by-step project instructions
├─ README.md
├─ .gitignore
└─ .venv
```

---

## 🛠️ Tech Stack

- **Python 3.13**
- **FastAPI** – REST API and server-side rendering
- **UV** – Fast, reproducible dependency management
- **Docker** – Containerization and image management
- **Kubernetes** – Container orchestration, scaling, and service exposure
- **Prometheus** – Metrics scraping, monitoring, and time-series storage
- **Grafana** – Metrics visualization and observability insights

---

## 📦 Prerequisites

Choose the setup based on how you want to run the application.

**Option 1: Running Locally (Without Docker)**

- Python 3.13
- [uv](https://uv.sh/) package manager
- Git

> This is only required if you want to run the API directly on your host machine.

**Option 2: Using Docker**

- Docker installed on your system.

> No need to install Python, uv, or packages locally. Docker contains everything.

**Option 3: Using Kubernetes (Minikube)**

- Docker
- Minikube
- kubectl

> Recommended if you want to test container orchestration, scaling, and service exposure locally using Kubernetes.
> Modify `deployment.yaml` and `service.yaml` file in k8s folder (if needed)

---

## 🚀 Quick Start Guide

#### 1. Clone the repository

```bash
git clone https://github.com/arpon-kapuria/k8s-observability-prometheus-grafana.git
cd k8s-observability-prometheus-grafana
```

#### 2. Install dependencies

```bash
# Using uv package manager
uv sync --locked

# This creates a .venv and installs all required packages.
```

#### 3. Run Locally (Without Docker)

```bash
# Run the FastAPI application locally 
uv run uvicorn src.app:app --host 0.0.0.0 --port 9696 --reload

# --host 0.0.0.0 makes it accessible from all network interfaces
# --port 9696 sets the port to 9696
# --reload enables automatic server reload when code changes
```

#### 4. Run with Docker

```bash
# Build the Docker image
docker build -t k8s-observability-prometheus-grafana:latest .

# Run the container (the --rm flag deletes the container automatically after it stops)
docker run -it --rm -p 9696:9696 k8s-observability-prometheus-grafana:latest
```

#### 5. Run with Kubernetes 

```bash
# Keep Docker running and start the Kubernetes cluster
minikube start

# Load the Docker image into minikube
minikube image load k8s-observability-prometheus-grafana:latest

# Deploy the Application
kubectl apply -f k8s/

# Access the Application
minikube service k8s-observability-prometheus-grafana
```

#### 6. Setup Prometheus

```bash
# Install Helm on macOS
brew install helm  

# Add Prometheus Helm Chart 
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts  
helm repo update  

# Install Prometheus
helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace    
```

#### 7. Configuring Prometheus to Scrape FastAPI Metrics  

```yaml  
# Retrieve FastAPI App Service IP
kubectl get svc  

# Note the ClusterIP and port for `k8s-observability-prometheus-grafana`. 

# Edit Prometheus ConfigMap

# To get the YAML editor 
kubectl edit configmap prometheus-server -n monitoring

# Add your FastAPI app as a scrape target in Prometheus configMap. 
scrape_configs:  
   - job_name: 'FastAPI-app'  
      static_configs:  
      - targets: ['CLUSTER-IP:PORT']  

# Restart Prometheus
kubectl rollout restart deployment prometheus-server -n monitoring  

# Access the Prometheus dashboard and search for FastAPI metrics
kubectl port-forward -n monitoring svc/prometheus-server 9090:80  
```

#### 8. Installing Grafana

```bash
# Add Grafana Helm Chart
helm repo add grafana https://grafana.github.io/helm-charts  
helm repo update  
  
# Install Grafana
helm install grafana grafana/grafana -n monitoring --create-namespace  

# Port-forward Grafana to your local machine 
kubectl port-forward svc/grafana -n monitoring 3000:80  
```
Log in with the default credentials:  
   - Username: `admin`  

```bash 
# To obtain Password 
kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode  
```

#### 9. Visualizing Metrics with Grafana Dashboards 

```bash
# Add Prometheus as a Data Source

Navigate to: `Connections > Data Sources > Add Data Source > Prometheus`  
Use Prometheus URL: `http://prometheus-server.monitoring.svc.cluster.local:80`

# Upon successful integration, visualise the metrics using dashboards  
```

~ At this point, You have a fully working local Kubernetes observability pipeline.


---

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
