# Build context: repo root  (fly deploy --dockerfile web/backend/Dockerfile)
FROM python:3.11-slim

WORKDIR /app

# Install system deps (gcc needed for some ply/clingo builds)
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY web/backend/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the xhail package source and install it
COPY xhail/ /app/xhail/
COPY pyproject.toml /app/
COPY README.md /app/
RUN pip install --no-cache-dir -e .

# Copy benchmark data so /learn and /benchmarks endpoints work
COPY experiments/benchmarks/ /app/experiments/benchmarks/

# Copy backend app
COPY web/backend/main.py /app/main.py

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
