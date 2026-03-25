from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def setup_opentelemetry(service_name: str = "ai-agent-platform", endpoint: str = "http://localhost:4317") -> None:
    """Initialize OpenTelemetry tracing and metrics."""
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource

    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=endpoint)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    logger.info("OpenTelemetry initialized", extra={"service": service_name, "endpoint": endpoint})


def get_tracer(name: str = "ai-agent-platform"):
    from opentelemetry import trace
    return trace.get_tracer(name)
