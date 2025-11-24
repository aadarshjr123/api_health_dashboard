from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter


def setup_tracing():
    provider = TracerProvider(
        resource=Resource.create({"service.name": "fastapi-service"})
    )

    jaeger_exporter = JaegerExporter(
        agent_host_name="jaeger",  # SERVICE name inside docker
        agent_port=6831,
    )

    provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
    trace.set_tracer_provider(provider)
