# Learning-Focused OpenTelemetry Zero-Code Observability Project

## Goal
Build a system where an application can enable/disable OpenTelemetry observability through configuration, without requiring application source-code changes wherever automatic instrumentation is supported.

## Core Architecture & Toggle
```
OTEL_ENABLED=true
    ↓
OpenTelemetry instrumentation is enabled
    ↓
Automatically collect:
- Traces
- Metrics
- Logs
    ↓
Send telemetry to an OpenTelemetry Collector
    ↓
Collector exports to observability backends such as:
- Prometheus for metrics
- Grafana for visualization
- Jaeger/Tempo for traces
- Loki or another backend for logs

OTEL_ENABLED=false
    ↓
Application runs normally without OpenTelemetry instrumentation.
```

> **Important**: This is primarily a learning project. We build it incrementally from a very small example and explain what each component does.

---

## Roadmap & Phases

### PHASE 1 — FASTAPI EXAMPLE
Create a simple FastAPI application with layered architecture:
```
Controller
    ↓
Service
    ↓
Repository
    ↓
PostgreSQL
```
- Example: `GET /users/{user_id}`
  - **Controller**: receives the HTTP request
  - **Service**: contains business logic
  - **Repository**: communicates with database
- Do **NOT** initially add manual OpenTelemetry spans to the application code.
- Run the application using OpenTelemetry Python zero-code instrumentation CLI:
  ```bash
  opentelemetry-instrument uvicorn main:app
  ```
- Investigate and demonstrate which telemetry is automatically generated.
- Determine whether OpenTelemetry automatically creates:
  `GET /users/{user_id} -> database query` and what information is available in those spans.

---

### PHASE 2 — UNDERSTAND THE LIMITATIONS
Clearly demonstrate the difference between:
1. **Automatic instrumentation**
2. **Manual / custom instrumentation**

Test whether OpenTelemetry automatically creates spans for:
- [ ] FastAPI endpoints
- [ ] Controller functions
- [ ] Service methods
- [ ] Repository methods
- [ ] PostgreSQL / Database queries
- [ ] Outgoing HTTP requests

*Do NOT assume that every application function will automatically become a span.*
Explain why framework/library boundaries can be instrumented automatically while custom business methods (such as `UserService.get_user()` and `UserRepository.find_user()`) may require custom instrumentation.

---

### PHASE 3 — OTEL ENABLE/DISABLE CONFIGURATION
Create a configuration-driven mechanism.
- `OTEL_ENABLED=true` &rarr; enable OpenTelemetry instrumentation.
- `OTEL_ENABLED=false` &rarr; application runs normally without telemetry.

Investigate standard OpenTelemetry environment variables:
- `OTEL_SERVICE_NAME`
- `OTEL_EXPORTER_OTLP_ENDPOINT`
- `OTEL_TRACES_EXPORTER`
- `OTEL_METRICS_EXPORTER`
- `OTEL_LOGS_EXPORTER`
- `OTEL_SDK_DISABLED`

Clearly distinguish between standard OpenTelemetry configuration and our own project-specific `OTEL_ENABLED` variable.

---

### PHASE 4 — OTEL COLLECTOR
Add an OpenTelemetry Collector.
```
FastAPI
   ↓
OpenTelemetry auto-instrumentation
   ↓
OTLP
   ↓
OpenTelemetry Collector
   ↓
--------------------------------
|              |               |
Metrics       Traces          Logs
|              |               |
Prometheus    Tempo/Jaeger    Loki
|              |               |
--------------------------------
             ↓
          Grafana
```
- Provide `docker-compose.yml` with the required services.

---

### PHASE 5 — GRAFANA
Configure Grafana to visualize the telemetry. Create a dashboard showing:
- **Metrics**: HTTP request count, HTTP request rate, HTTP request duration, error count, application/process metrics.
- **Traces**: HTTP request traces, database spans, trace duration, errors.
- **Logs**: Application logs, error logs, trace/span correlation where supported.

---

### PHASE 6 — CROSS-LANGUAGE INVESTIGATION
Investigate how zero-code/automatic instrumentation works for:
- Python
- Java
- .NET
- JavaScript / Node.js
- Go (where applicable)

For each language, document:
1. How OpenTelemetry is installed
2. How automatic instrumentation is enabled
3. Whether an agent is used
4. Whether monkey patching is used
5. Whether bytecode/runtime instrumentation is used
6. How the application is started
7. How `OTEL_ENABLED`-style configuration can be achieved
8. What can and cannot be automatically instrumented

---

### PHASE 7 — APPLICATION-LEVEL INSTRUMENTATION
After understanding zero-code instrumentation, add an experiment for custom business logic:
```
Controller -> UserService.get_user() -> UserRepository.find_user() -> PostgreSQL
```
Compare:
- **A**: Zero-code instrumentation
- **B**: Manual instrumentation
- **C**: A possible automatic/custom mechanism for instrumenting application methods

Determine which approach is practical and portable across languages.

---

## Important Requirements
1. Do not modify application code unnecessarily.
2. Prefer zero-code OpenTelemetry instrumentation where supported.
3. Do not claim that OpenTelemetry automatically instruments every function in an application.
4. Clearly distinguish framework, library, database, and custom application instrumentation.
5. Use official OpenTelemetry documentation as the primary reference.
6. Explain every step because this is a learning project.
7. Start with the smallest possible working example.
8. Do not build the entire system at once.
9. After each phase, verify that it works before moving to the next phase.
10. Show commands for Windows because the development environment is Windows + Docker Desktop.
11. Keep the architecture simple initially and increase complexity gradually.

---

## Expected Learning Outcome
By the end, you should understand:
1. What OpenTelemetry actually does.
2. How zero-code instrumentation works.
3. How monkey patching/agents/runtime instrumentation are used.
4. What OpenTelemetry automatically detects.
5. What requires manual instrumentation.
6. How traces, metrics, and logs differ.
7. How OTLP works.
8. What the OpenTelemetry Collector does.
9. How Prometheus and Grafana fit into the architecture.
10. How the same observability concept can be applied to different programming languages.
11. Whether a single configuration switch such as `OTEL_ENABLED=true` can practically control observability without changing application source code.
