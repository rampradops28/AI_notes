# 1. Manual OpenTelemetry Instrumentation (For Absolute Beginners)

In this project, you see how OpenTelemetry works by manually wrapping your code in **Spans** and printing them directly to your terminal.

## What is Inside `main.py`?

There are only **4 core concepts**:
1. **`Resource`**: Names your service (`service.name = "pizza-store"`).
2. **`TracerProvider`**: The central factory engine.
3. **`ConsoleSpanExporter`**: Prints spans to your terminal in JSON.
4. **`with tracer.start_as_current_span("operation_name") as span:`**: Creates a timed box of work.

## How to Run

### Method 1: Instant In-Process Test (Recommended!)
Run this single command:
```bash
python test_app.py
```
Watch your terminal! It will make a request and print the Spans in JSON format, showing:
- **`trace_id`**: Shared by all spans in the order.
- **`parent_id`**: How child spans (`make_dough`, `bake_oven`) link to the root (`order_pizza`).
- **`attributes`**: Metadata like `"pizza.type": "pepperoni"`.
- **`events`**: Milestones like `"dough_kneaded"`.

### Method 2: Run as a Web Server
```bash
python main.py
```
Open your browser to:
- `http://127.0.0.1:8000/pizza/pepperoni?quantity=2`
- `http://127.0.0.1:8000/burn-pizza`

Look at your terminal to see the spans print in real time!
