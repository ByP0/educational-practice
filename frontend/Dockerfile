FROM node:20-alpine AS build

RUN mkdir /app

WORKDIR /app

COPY ./ /app

RUN npm install -g npm@11.3.0

RUN npm install 

RUN npm install vite-plugin-compression --save-dev

EXPOSE 3000

CMD ["npm", "run", "dev"]