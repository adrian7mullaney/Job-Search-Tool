# syntax=docker/dockerfile:1.3
FROM python:3.10-slim as backend-builder

WORKDIR /app
COPY requirements.txt . 
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app/

FROM node:14-alpine as frontend-builder

WORKDIR /app
COPY cv-builder-frontend/package*.json ./cv-builder-frontend/
RUN npm install --prefix cv-builder-frontend
COPY cv-builder-frontend ./cv-builder-frontend
RUN npm run build --prefix cv-builder-frontend

FROM python:3.10-slim as backend

WORKDIR /app
COPY --from=backend-builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY . /app/
EXPOSE 5000 6379
RUN pip install supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

FROM nginx:stable-alpine as frontend

COPY --from=frontend-builder /app/cv-builder-frontend/build /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

FROM backend as final
COPY --from=frontend /usr/share/nginx/html /app/cv-builder-frontend/build
CMD ["/usr/local/bin/supervisord", "-n"]
