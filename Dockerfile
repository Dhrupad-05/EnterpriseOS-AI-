FROM python:3.11-slim AS builder
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir --prefix=/install .

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY app app
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000","--timeout-keep-alive","30"]
