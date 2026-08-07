import logging
try:
    import structlog
except ImportError:
    structlog = None
def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    if structlog:
        structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.INFO), logger_factory=structlog.PrintLoggerFactory())
