FROM node:latest AS build

WORKDIR /app

COPY front_it_school/package*.json ./

RUN npm install --force

COPY front_it_school/ ./

RUN npm run build

FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

COPY docker/frontend/nginx.conf /etc/nginx/nginx.conf

COPY --from=build /app/build/ /usr/share/nginx/html/