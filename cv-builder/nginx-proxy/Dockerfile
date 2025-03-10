# syntax=docker/dockerfile:1.3
FROM nginx:stable-alpine AS base

FROM base AS config
COPY nginx.conf /etc/nginx/conf.d/default.conf

FROM config AS final
EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]
