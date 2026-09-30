"""
Instant In-Process Test Runner for Manual OpenTelemetry
======================================================
Run this anytime:
    python test_app.py

It makes requests to the FastAPI app without needing a background server,
and prints the resulting OpenTelemetry Spans directly to your screen!
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("\n" + "=" * 70)
print("  TEST 1: Making a Pepperoni Pizza (Watch the Spans get printed below!)")
print("=" * 70)
response = client.get("/pizza/pepperoni?quantity=2")
print(f"HTTP Response: {response.status_code} -> {response.json()}\n")

print("=" * 70)
print("  TEST 2: Triggering an Error (Watch the Error Span get printed below!)")
print("=" * 70)
err_response = client.get("/burn-pizza")
print(f"HTTP Response: {err_response.status_code} -> {err_response.json()}\n")

print("=" * 70)
print("  WHAT YOU JUST OBSERVED:")
print("  1. 'make_dough' and 'bake_oven' spans were printed with start/end times.")
print("  2. 'order_pizza' was the parent span with custom attributes.")
print("  3. The error span captured the Python exception stack trace!")
print("=" * 70 + "\n")
