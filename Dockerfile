# Stage 1: Build
FROM python:3.13-alpine as builder

WORKDIR /app
COPY requirements.txt .

RUN pip install --user --no-warn-script-location -r requirements.txt

# Stage 2: Runtime
FROM python:3.13-alpine

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]