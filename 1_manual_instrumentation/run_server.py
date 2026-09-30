"""
Run Manual Instrumentation FastAPI Server -> Grafana Tempo
===========================================================
Launches the Pizza Store server on port 8000.
"""

import subprocess
import sys


def main():
    print("=" * 70)
    print("  MANUAL OPENTELEMETRY PIZZA STORE SERVER")
    print("  - Swagger UI (Execute APIs): http://127.0.0.1:8000/docs")
    print("  - Grafana Dashboard:         http://localhost:3000")
    print("=" * 70)

    subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"])


if __name__ == "__main__":
    main()
