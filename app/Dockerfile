# =========================
# Stage 1: Build
# =========================
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

# Update OS packages and install Python dependencies
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# =========================
# Stage 2: Production
# =========================
FROM python:3.12-slim-bookworm

WORKDIR /app

# Update OS packages
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Create non-root application user
RUN useradd --create-home --shell /usr/sbin/nologin appuser

# Copy Python dependencies
COPY --from=builder /install /usr/local

# Copy application
COPY app.py .

# Run application as non-root user
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
