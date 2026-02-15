from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
import random

app = FastAPI(title="k8s-observability-prometheus-grafana")

# Simulated metrics
total_requests = 0

@app.get("/metrics", status_code=200)
def metrics():
    global total_requests
    total_requests += 1

    # Simulated values
    request_processing_latency = round(random.uniform(0.1, 1.5), 3) # Latency in seconds
    model_prediction_success_rate = round(random.uniform(80, 100), 2) # Success rate in % 

    # Return the metrics in Prometheus format
    prometheus_metrics = (
        f"# HELP total_api_requests_total Total number of API requests\n"
        f"# TYPE total_api_requests_total counter\n"
        f"total_api_requests_total {total_requests}\n"
        f"\n"
        f"# HELP request_processing_latency_seconds Latency for request processing\n"
        f"# TYPE request_processing_latency_seconds gauge\n"
        f"request_processing_latency_seconds {request_processing_latency}\n"
        f"\n"
        f"# HELP model_prediction_success_rate Model prediction success rate\n"
        f"# TYPE model_prediction_success_rate gauge\n"
        f"model_prediction_success_rate {model_prediction_success_rate}\n"        
    )

    return Response(
        content=prometheus_metrics,
        media_type="text/plain; charset=utf-8"
    )


@app.get("/")
def index():
    return JSONResponse(
        content={
            "message": "Welcome to the FastAPI Metrics App! Access /metrics for Prometheus metrics."
        }
    )
