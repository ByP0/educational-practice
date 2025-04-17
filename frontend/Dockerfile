FROM node:16.18-alpine

WORKDIR /usr/src/frontend_app

COPY package*.json ./

RUN npm install --legacy-peer-deps

RUN npm install -g vite

COPY . .

EXPOSE 3000

RUN ls -la ./node_modules/.bin

CMD ["npm", "run", "dev"]