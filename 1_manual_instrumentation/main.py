"""
==============================================================================
 OpenTelemetry: 1. Manual Instrumentation
==============================================================================
 WHAT IS A SPAN?
 A Span is a timed box of work. It records:
   - What the operation was named (e.g., 'bake_pizza')
   - When it started and when it ended (its duration)
   - Extra data/tags called Attributes (e.g., pizza.type = "pepperoni")
   - Milestone breadcrumbs called Events (e.g., "cheese_melted")

 WHAT IS A TRACE?
 A Trace is simply the tree of all Spans that happened during one user request!

 WHY CONSOLE EXPORTER?
 For beginners, we print spans directly to this terminal! No Docker or Jaeger
 needed. You will see the exact JSON data that OpenTelemetry creates!
==============================================================================
"""

import time
from fastapi import FastAPI, HTTPException
import uvicorn

# ------------------------------------------------------------------------------
# STEP 1: Setup OpenTelemetry (The 4 Basic Concepts)
# ------------------------------------------------------------------------------
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

# 1. Resource: Who is producing this telemetry?
resource = Resource.create(attributes={"service.name": "pizza-store"})

# 2. TracerProvider: The factory that creates and manages tracers
provider = TracerProvider(resource=resource)

# 3. Exporter: Where should the spans go?
#    a) ConsoleSpanExporter prints spans directly to your terminal
console_exporter = ConsoleSpanExporter()
provider.add_span_processor(SimpleSpanProcessor(console_exporter))

#    b) OTLPSpanExporter sends spans to Grafana Tempo if running on port 4318
try:
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
    provider.add_span_processor(SimpleSpanProcessor(otlp_exporter))
except Exception:
    pass

# Register as the global default tracer provider
trace.set_tracer_provider(provider)

# Create a Tracer to use in our code
tracer = trace.get_tracer("pizza-store-tracer")


# ------------------------------------------------------------------------------
# STEP 2: Standard FastAPI App
# ------------------------------------------------------------------------------
app = FastAPI(
    title="Beginner Pizza Store (Manual OpenTelemetry)",
    description="Learn OpenTelemetry with simple, readable spans printed to terminal.",
)


# ------------------------------------------------------------------------------
# STEP 3: Route with Parent and Child Spans
# ------------------------------------------------------------------------------
@app.get("/pizza/{pizza_type}")
def make_pizza(pizza_type: str, quantity: int = 1):
    """
    Simulates making a pizza.
    Notice how we use `with tracer.start_as_current_span(...)` to measure time and add tags!
    """

    # 1. ROOT SPAN: Represents the whole pizza order
    with tracer.start_as_current_span("order_pizza") as order_span:
        
        # ATTRIBUTES: Useful key-value tags attached to the span
        order_span.set_attribute("pizza.type", pizza_type)
        order_span.set_attribute("pizza.quantity", quantity)
        order_span.set_attribute("customer.tier", "vip")

        # 2. CHILD SPAN 1: Step 1 - Making the dough
        with tracer.start_as_current_span("make_dough") as dough_span:
            dough_span.set_attribute("dough.flour", "organic_wheat")
            time.sleep(0.1)  # Simulate dough preparation time
            
            # EVENT: A point-in-time milestone inside a span
            dough_span.add_event("dough_kneaded", {"consistency": "perfect"})

        # 3. CHILD SPAN 2: Step 2 - Baking in the oven
        with tracer.start_as_current_span("bake_oven") as oven_span:
            oven_span.set_attribute("oven.temperature_celsius", 350)
            time.sleep(0.2)  # Simulate baking time
            
            oven_span.add_event("baking_finished")

        return {
            "message": f"Your {quantity} {pizza_type} pizza is ready!",
            "status": "delicious",
            "hint": "Check your terminal to see the OpenTelemetry spans printed!"
        }


# ------------------------------------------------------------------------------
# STEP 4: Error Handling in Spans
# ------------------------------------------------------------------------------
@app.get("/burn-pizza")
def burn_pizza():
    """Demonstrates how OpenTelemetry automatically catches errors and marks spans."""
    with tracer.start_as_current_span("risky_cooking_task") as span:
        try:
            span.set_attribute("oven.temperature_celsius", 900)
            # Simulate a failure
            raise ValueError("Oven caught on fire! Pizza is destroyed.")
        except Exception as exc:
            # 1. Record the exception (saves the stacktrace into the span)
            span.record_exception(exc)
            # 2. Mark the span status as ERROR (shows red in dashboards)
            span.set_status(trace.StatusCode.ERROR, description=str(exc))
            raise HTTPException(status_code=500, detail=str(exc))


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  PIZZA STORE RUNNING ON: http://127.0.0.1:8000")
    print("  Try opening in your browser: http://127.0.0.1:8000/pizza/pepperoni")
    print("  Look at this terminal to see the Spans printed in real-time!")
    print("=" * 60 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
