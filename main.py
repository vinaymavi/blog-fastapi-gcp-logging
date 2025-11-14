import structlog
from fastapi import FastAPI, Request
import os
import logging
import sys

# Configure standard logging to stdout
logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)

# Custom processor to map log levels to GCP severity
def add_gcp_severity(logger, method_name, event_dict):
    """
    Add GCP-compatible severity field based on log level.
    GCP Cloud Logging recognizes: DEFAULT, DEBUG, INFO, NOTICE, WARNING, ERROR, CRITICAL, ALERT, EMERGENCY
    """
    level = event_dict.get("level", "").upper()
    
    # Map Python log levels to GCP severity levels
    severity_mapping = {
        "DEBUG": "DEBUG",
        "INFO": "INFO",
        "WARNING": "WARNING",
        "ERROR": "ERROR",
        "CRITICAL": "CRITICAL",
    }
    
    # Add severity field for GCP
    event_dict["severity"] = severity_mapping.get(level, "DEFAULT")
    
    return event_dict

# Configure structlog to output JSON to stdout with GCP severity
# GCP Cloud Logging automatically ingests JSON logs from stdout
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        add_gcp_severity,  # Add GCP severity mapping
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

app = FastAPI(title="FastAPI GCP Logging Example")
logger = structlog.get_logger()


@app.api_route("/debug", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def debug_log(request: Request):
    """Log at DEBUG level"""
    body = await request.body()
    logger.debug(
        "Debug level log",
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host,
        body=body.decode() if body else None
    )
    return {"level": "DEBUG", "message": "Logged at DEBUG level", "method": request.method}


@app.api_route("/info", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def info_log(request: Request):
    """Log at INFO level"""
    body = await request.body()
    logger.info(
        "Info level log",
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host,
        body=body.decode() if body else None
    )
    return {"level": "INFO", "message": "Logged at INFO level", "method": request.method}


@app.api_route("/warning", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def warning_log(request: Request):
    """Log at WARNING level"""
    body = await request.body()
    logger.warning(
        "Warning level log",
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host,
        body=body.decode() if body else None
    )
    return {"level": "WARNING", "message": "Logged at WARNING level", "method": request.method}


@app.api_route("/error", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def error_log(request: Request):
    """Log at ERROR level"""
    body = await request.body()
    logger.error(
        "Error level log",
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host,
        body=body.decode() if body else None
    )
    return {"level": "ERROR", "message": "Logged at ERROR level", "method": request.method}


@app.api_route("/critical", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def critical_log(request: Request):
    """Log at CRITICAL level"""
    body = await request.body()
    logger.critical(
        "Critical level log",
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host,
        body=body.decode() if body else None
    )
    return {"level": "CRITICAL", "message": "Logged at CRITICAL level", "method": request.method}


@app.get("/")
async def root():
    """Root endpoint with API information"""
    logger.info("Root endpoint accessed")
    return {
        "message": "FastAPI GCP Logging Example",
        "endpoints": {
            "/debug": "Log at DEBUG level",
            "/info": "Log at INFO level",
            "/warning": "Log at WARNING level",
            "/error": "Log at ERROR level",
            "/critical": "Log at CRITICAL level"
        },
        "note": "All endpoints accept GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD methods"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
