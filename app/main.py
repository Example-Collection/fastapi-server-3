from fastapi import FastAPI, Request
from app.service import handle_request_from_server_2
from app.otel import tracer
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.instrumentation.logging import LoggingInstrumentor
import logging


app = FastAPI()

LoggingInstrumentor().instrument(set_logging_format=True,
                                 logging_format=' trace_id=%(otelTraceID)s span_id=%(otelSpanID)s - %(message)s')


def get_trace_parent_header(request: Request):
    return request.headers.get("traceparent")


@app.get("/items-price-check", status_code=200)
async def server_3_handler(price: float = 0.0, request: Request = None):
    traceparent = get_trace_parent_header(request)
    carrier = {"traceparent": traceparent}
    ctx = TraceContextTextMapPropagator().extract(carrier)
    with tracer.start_as_current_span("server-3-handler", context=ctx)as span:
        span.set_attribute("item_price", price)
        span.set_attribute("ip", request.client.host)
        span.set_attribute("path", request.url.path)
        logging.warning(f"[SERVER-3] Received item price: {price}")
        return handle_request_from_server_2(item_price=price)
