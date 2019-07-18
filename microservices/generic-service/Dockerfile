FROM node:8

WORKDIR /usr/src/app

RUN apt-get update

COPY package*.json ./

RUN npm install
RUN npm install nodemon -g

COPY . ./

# Change to npm start for deploy
CMD ["nodemon"]
