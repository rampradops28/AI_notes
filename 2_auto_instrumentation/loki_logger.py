"""
OpenTelemetry Logging Setup for Loki
====================================
Hooks standard Python and Uvicorn loggers to the active OpenTelemetry LoggerProvider,
shipping logs directly to Loki with trace-context correlation!
"""

import logging
from opentelemetry._logs import get_logger_provider
from opentelemetry.sdk._logs import LoggingHandler

# Attach LoggingHandler using the existing OpenTelemetry LoggerProvider
logger_provider = get_logger_provider()
handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)

# Register on root and uvicorn loggers
logging.getLogger().addHandler(handler)
logging.getLogger("uvicorn").addHandler(handler)
logging.getLogger("uvicorn.access").addHandler(handler)
