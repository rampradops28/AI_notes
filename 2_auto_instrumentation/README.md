# 2. Auto-Instrumentation (Zero Code Changes)

In this project, your FastAPI code has **ZERO OpenTelemetry code**.

## What is Inside `main.py`?
Look at `main.py`:
- There is NO `import opentelemetry`
- There are NO spans or tracers
- It is just ordinary FastAPI endpoints: `/books/{book_id}` and `/search`.

## How Auto-Instrumentation Works

Instead of modifying your Python file, OpenTelemetry automatically hooks into FastAPI at runtime!

### Method 1: Instant In-Process Test (Recommended!)
Run:
```bash
python test_app.py
```
Watch your terminal! It will automatically intercept the request and print the server spans without a single line of telemetry in `main.py`.

### Method 2: Running via the CLI Agent
Run this command in your terminal:
```bash
opentelemetry-instrument --traces_exporter console uvicorn main:app --port 8000
```
Then visit:
- `http://127.0.0.1:8000/books/1`
- `http://127.0.0.1:8000/search?q=Clean`

Watch your terminal print the auto-generated spans in real-time!
