"""
Instant In-Process Test Runner for Phase 1 Layered Flow
======================================================
Run this anytime:
    python test_app.py

Demonstrates:
  Controller -> Service -> Repository -> PostgreSQL
Instruments FastAPI automatically and prints the generated Spans to console!
"""

from fastapi.testclient import TestClient
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# 1. Import our 100% vanilla FastAPI app and database engine
from main import app
from database import engine

# 2. Setup the Console Exporter
provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)

# 3. Auto-instrument FastAPI and SQLAlchemy
FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=engine)

# 4. Make requests using TestClient
client = TestClient(app)

print("\n" + "=" * 70)
print("  TEST 1: Requesting GET /users/1 (Controller -> Service -> Repo -> DB)")
print("=" * 70)
response = client.get("/users/1")
print(f"HTTP Response: {response.status_code} -> {response.json()}\n")

print("=" * 70)
print("  TEST 2: Requesting POST /users (Insert new user into PostgreSQL)")
print("=" * 70)
post_resp = client.post("/users", json={"name": "Diana Prince", "email": "diana@example.com", "role": "lead"})
print(f"HTTP Response: {post_resp.status_code} -> {post_resp.json()}\n")

print("=" * 70)
print("  TEST 3: Requesting GET /users (Query all users from PostgreSQL)")
print("=" * 70)
list_resp = client.get("/users")
print(f"HTTP Response: {list_resp.status_code} -> Count: {len(list_resp.json())}\n")

print("=" * 70)
print("  OBSERVATION FOR PHASE 1 & 2:")
print("  - Look at the Spans printed above!")
print("  - OpenTelemetry automatically intercepted:")
print("      * HTTP Span: GET /users/{user_id}")
print("      * DB Span:   SELECT users.id, users.name... FROM users WHERE users.id = %(id_1)s")
print("  - NOTICE WHAT IS MISSING:")
print("      * UserService.get_user() did NOT generate a span!")
print("      * UserRepository.get_by_id() did NOT generate a span!")
print("      Why? Because OpenTelemetry auto-instruments LIBRARY/FRAMEWORK boundaries")
print("      (FastAPI, SQLAlchemy), NOT arbitrary internal Python functions!")
print("=" * 70 + "\n")
