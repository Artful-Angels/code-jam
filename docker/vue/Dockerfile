FROM node:lts-alpine
RUN apk add git  # For developing through the container

WORKDIR /app
# COPY ./frontend/package*.json ./frontend
COPY . .

WORKDIR /app/frontend
RUN npm install


EXPOSE 8080
CMD [ "npm", "run", "dev" ]
