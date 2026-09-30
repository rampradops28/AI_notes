"""
Run FastAPI Server with Auto-Instrumentation -> Grafana LGTM
============================================================
Launches the server on port 8000 (or 8001 if 8000 is occupied/locked)
and exports traces directly to Grafana Tempo (http://localhost:4318/v1/traces)
and metrics to Prometheus (http://localhost:4318/v1/metrics).
"""

import os
import socket
import subprocess
import sys

# 1. OpenTelemetry Standard Environment Configuration
os.environ["OTEL_SERVICE_NAME"] = "book-store"
os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = "http/protobuf"

# Export Traces to Tempo
os.environ["OTEL_TRACES_EXPORTER"] = "otlp"
os.environ["OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"] = "http://localhost:4318/v1/traces"

# Export Metrics to Prometheus
os.environ["OTEL_METRICS_EXPORTER"] = "otlp"
os.environ["OTEL_EXPORTER_OTLP_METRICS_ENDPOINT"] = "http://localhost:4318/v1/metrics"
os.environ["OTEL_METRIC_EXPORT_INTERVAL"] = "5000"  # Flush every 5s

# Export Logs to Loki
os.environ["OTEL_LOGS_EXPORTER"] = "otlp"
os.environ["OTEL_EXPORTER_OTLP_LOGS_ENDPOINT"] = "http://localhost:4318/v1/logs"

os.environ["OTEL_PYTHON_LOG_CORRELATION"] = "true"


def find_available_port(preferred_port=8000):
    for port in [preferred_port, 8001, 8002, 8080]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return preferred_port


def main():
    port = find_available_port(8000)

    print("=" * 70)
    print("  FASTAPI SERVER WITH OPENTELEMETRY AUTO-INSTRUMENTATION")
    print(f"  - Swagger UI (Execute APIs): http://127.0.0.1:{port}/docs")
    print("  - Grafana Dashboard:         http://localhost:3000")
    if port != 8000:
        print(f"  [Note] Port 8000 was busy, automatically switched to port {port}!")
    print("=" * 70)

    cmd = [
        "opentelemetry-instrument",
        sys.executable,
        "-m",
        "uvicorn",
        "main:app",
        "--host",
        "127.0.0.1",
        "--port",
        str(port),
    ]
    try:
        subprocess.run(cmd)
    except FileNotFoundError:
        # Fallback if opentelemetry-instrument binary is not in PATH
        subprocess.run(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "main:app",
                "--host",
                "127.0.0.1",
                "--port",
                str(port),
            ]
        )


if __name__ == "__main__":
    main()
