"""
Instant In-Process Test Runner for Auto-Instrumentation
======================================================
Run this anytime:
    python test_app.py

It activates the OpenTelemetry FastAPI auto-instrumentor on our vanilla app
and prints the automatically generated Spans directly to your terminal!
"""

from fastapi.testclient import TestClient
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# 1. Import our 100% vanilla FastAPI app (which has NO telemetry code inside it!)
from main import app

# 2. Setup the Console Exporter so we can see spans in the terminal
provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)

# 3. THE MAGIC OF AUTO-INSTRUMENTATION:
# One single line instruments the entire application automatically!
FastAPIInstrumentor.instrument_app(app)

# 4. Make requests using TestClient
client = TestClient(app)

print("\n" + "=" * 70)
print("  TEST 1: Requesting /books/1 (Auto-Instrumentation generates span!)")
print("=" * 70)
response = client.get("/books/1")
print(f"HTTP Response: {response.status_code} -> {response.json()}\n")

print("=" * 70)
print("  TEST 2: Searching /search?q=Clean")
print("=" * 70)
search_resp = client.get("/search?q=Clean")
print(f"HTTP Response: {search_resp.status_code} -> {search_resp.json()}\n")

print("=" * 70)
print("  WHAT YOU JUST OBSERVED:")
print("  - main.py has ZERO OpenTelemetry code!")
print("  - OpenTelemetry automatically intercepted the HTTP routes:")
print("      * HTTP Method: GET")
print("      * HTTP Route: /books/{book_id}")
print("      * HTTP Status Code: 200")
print("      * Execution Duration in milliseconds")
print("=" * 70 + "\n")
