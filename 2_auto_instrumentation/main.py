"""
==============================================================================
 OpenTelemetry: 2. Auto-Instrumentation (Zero-Code)
==============================================================================
 LOOK CLOSELY AT THIS FILE:
 - There is NO 'import opentelemetry'
 - There is NO 'tracer = ...'
 - There is NO 'with tracer.start_as_current_span(...)'

 This is 100% standard, ordinary FastAPI code!

 HOW AUTO-INSTRUMENTATION WORKS:
 Instead of modifying your Python code, you launch this app with the
 OpenTelemetry CLI runner:

     opentelemetry-instrument --traces_exporter console uvicorn main:app

 OpenTelemetry automatically hooks into FastAPI, inspects every incoming route,
 measures the exact response time, and prints the generated Spans!
==============================================================================
"""

import logging
import time
from fastapi import FastAPI, HTTPException

# Optional: ship logs to Loki via OTLP
try:
    import loki_logger
except Exception:
    pass

logger = logging.getLogger("book-store")

app = FastAPI(
    title="Beginner Book Store (Auto-Instrumentation)",
    description="This code has ZERO telemetry imports. Everything is traced automatically!",
)

# Simulated database
books_db = {
    "1": {"title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann", "price": 45.00},
    "2": {"title": "Clean Code", "author": "Robert C. Martin", "price": 38.50},
    "3": {"title": "Fluent Python", "author": "Luciano Ramalho", "price": 52.00},
}


@app.get("/")
def home():
    logger.info("Home endpoint requested")
    return {"message": "Welcome to the Book Store! Visit /books/1 to see auto-tracing in action."}


@app.get("/books/{book_id}")
def get_book(book_id: str):
    logger.info("Fetching book with ID: %s", book_id)
    time.sleep(0.05)

    if book_id not in books_db:
        logger.warning("Book ID %s was not found in database", book_id)
        raise HTTPException(status_code=404, detail="Book not found")

    return {"book_id": book_id, "data": books_db[book_id]}


@app.get("/search")
def search_books(q: str = ""):
    logger.info("Searching books for query: '%s'", q)
    time.sleep(0.03)
    results = [b for b in books_db.values() if q.lower() in b["title"].lower()]
    return {"query": q, "count": len(results), "results": results}

