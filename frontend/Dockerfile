FROM node:alpine AS builder
WORKDIR /app
COPY . .
RUN npm ci
RUN npm run build

FROM nginx:alpine
RUN apk add --no-cache nodejs npm supervisor
COPY --from=builder /app/dist /usr/share/nginx/html
COPY ./proxy/default.conf /etc/nginx/conf.d/default.conf
COPY ./proxy/fullstackwebdev.pem /etc/nginx/ssl/fullstackwebdev.pem
COPY ./proxy/fullstackwebdevkey.pem /etc/nginx/ssl/fullstackwebdevkey.pem
EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]
