# FastAPI + OpenTelemetry + Grafana Dashboard

This guide walks you through:
1. Running the **FastAPI Server**.
2. Testing endpoints directly in **Swagger UI** (`/docs`).
3. Viewing your live request traces inside the **Grafana Dashboard** (`http://localhost:3000`).

---

## Architecture Flow

```
1. You click "Execute" in Swagger UI (http://127.0.0.1:8000/docs)
      │
      ▼
2. FastAPI Server processes the request
      │
      ▼ (OpenTelemetry exports spans via OTLP to port 4318)
3. Grafana Tempo stores the traces (port 3200)
      │
      ▼
4. You view the trace waterfall in Grafana Dashboard (http://localhost:3000/explore)
```

---

## 3-Step Setup Guide

### Step 1: Start the All-in-One LGTM Stack (Grafana + Tempo + Loki + Prometheus)
Make sure Docker Desktop is running, then start the container:

```powershell
docker run -d --name lgtm -p 3000:3000 -p 4317:4317 -p 4318:4318 -e GF_AUTH_ANONYMOUS_ENABLED=true -e GF_AUTH_ANONYMOUS_ORG_ROLE=Admin grafana/otel-lgtm:latest
```
*(If already started, this is already active and healthy on your machine!)*

*This boots up:*
- **Grafana** on `http://localhost:3000` (auto-login enabled as Admin, no password prompt).
- **Tempo** on OTLP HTTP port `4318` and gRPC port `4317` (pre-wired to Grafana with zero config).

---

### Step 2: Run the FastAPI Server (Auto-Instrumented)
In another terminal, run:

```powershell
cd c:\Workspace\FastAPI\fastapi_otel\2_auto_instrumentation
python run_server.py
```
*Your terminal will confirm:*
```text
  🚀 FASTAPI SERVER READY FOR TESTING
  1. Swagger UI (Execute APIs): http://127.0.0.1:8000/docs
  2. Grafana Dashboard:         http://localhost:3000
```

---

### Step 3: Test in Swagger UI & Inspect in Grafana

#### A. Execute APIs in Swagger UI:
1. Open your browser to **`http://127.0.0.1:8000/docs`**.
2. Expand **`GET /books/{book_id}`**.
3. Click **Try it out**, enter `book_id: 1`, and click **Execute**.
4. Expand **`GET /search`**, enter `q: Clean`, and click **Execute**.

#### B. View Traces in Grafana:
1. Open your browser to **`http://localhost:3000/explore`**.
2. **Tempo** is already selected as the Data Source!
3. Under Query Type, select **Search**.
4. In **Service Name**, choose `book-store`.
5. Click the blue button **Run query** (top right corner).
6. Click any trace in the search results table to view the full visual waterfall!
