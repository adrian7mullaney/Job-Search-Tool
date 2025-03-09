# Dockerfile (for backend)
FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app/

FROM python:3.9-slim
WORKDIR /app
# Copy Python packages from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . /app/
EXPOSE 5000 6379
RUN pip install supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/local/bin/supervisord", "-n"]
