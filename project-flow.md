#  Project Flow

#### ~ Run app locally
1) Prepare the FastAPI application locally  
Ensure the app runs correctly and exposes metrics (e.g., `/metrics`).

#### ~ Deploy FastAPI on Minikube

2) Start Docker engine.

3) Build the Docker image:
```bash
docker build -t k8s-observability-prometheus-grafana .
```

4) Create Kubernetes manifest files inside a `k8s/` directory.

5) Start Minikube:
```bash
minikube start
```

6) Load the image into the cluster:
```bash
minikube image load k8s-observability-prometheus-grafana:latest
```

7) Apply Kubernetes manifests:
```bash
kubectl apply -f k8s/
```

8) Get the FastAPI service URL:
```bash
minikube service k8s-observability-prometheus-grafana --url
```

#### ~ Install Prometheus using Helm

9) Install Helm.

10)    Verify installation:
```bash
helm version
```

11)   Add Prometheus Helm repository:
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts  
helm repo update  
helm search repo prometheus
```

12)   Install Prometheus in a monitoring namespace:
```bash
helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace
```

#### ~ Access Prometheus Dashboard

13)   List services in the monitoring namespace:
```bash
kubectl get svc -n monitoring
```

14)   Port-forward Prometheus locally:
```bash
kubectl port-forward -n monitoring svc/prometheus-server 9090:80
```

15)   Open: http://localhost:9090

#### ~ Configure Prometheus to Scrape FastAPI

16)   Get FastAPI service details:
```bash
kubectl get svc
```
Note the ClusterIP and port of `k8s-observability-prometheus-grafana`.

*Example:* `10.107.61.186`<span style="margin-left:30px;"></span>`5000/TCP`

17) Edit Prometheus ConfigMap:
```bash
kubectl edit configmap prometheus-server -n monitoring
```

18) Under `scrape_configs`, add:
```yaml
scrape_configs:
  - job_name: 'fastapi-app'
    static_configs:
      - targets: ['10.107.61.186:5000']
```

#### ~ Restart Prometheus

***Option 1** — Restart Pod*

19) Check labels:
```bash
kubectl get pods -n monitoring --show-labels
```

20) Delete Prometheus pod using correct label:
```bash
kubectl delete pod -l app.kubernetes.io/name=prometheus -n monitoring
```

21) Verify restart:
```bash
kubectl get pods -n monitoring
```

***Option 2** — Restart Deployment*
```bash
kubectl get deploy -n monitoring  
kubectl rollout restart deployment prometheus-server -n monitoring  
kubectl get pods -n monitoring
```

#### ~ Verify Metrics Collection

22) Port-forward again:
```bash
kubectl port-forward -n monitoring svc/prometheus-server 9090:80
```

23) In Prometheus UI, search for a metric such as `total_api_requests_total`. If visible, scraping is successful.

#### ~ Install Grafana

1)  Add Grafana Helm repo:
```bash
helm repo add grafana https://grafana.github.io/helm-charts  
helm repo update
```

25) Install Grafana:
```bash
helm install grafana grafana/grafana -n monitoring --create-namespace
```

26) Check installation:
```bash
kubectl get pods -n monitoring  
kubectl get svc -n monitoring
```

27) Port-forward Grafana locally:
```bash
kubectl port-forward svc/grafana -n monitoring 3000:80
```
28) Open: http://localhost:3000

29) Login to Grafana. Decode the Base64 string manually *(For windows)*

```bash
Username: admin  

Get password (Linux/macOS):

kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

Windows PowerShell:

kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}"
```

#### ~ Add Prometheus as Data Source

30) After login:

Connections → Data Sources → Add Data Source → Prometheus

Use internal service URL:

http://prometheus-server.monitoring.svc.cluster.local:80

31) Click “Save & Test”.

32) Create Dashboards
```bash
Go to:

Dashboard → New Dashboard → Add Panel

Enter a metric name (e.g., total_api_requests_total) 
run the query → save the dashboard.
```
---

At this point, the stack is complete:

FastAPI → Metrics → Prometheus → Grafana

You now have a fully working local Kubernetes observability pipeline.