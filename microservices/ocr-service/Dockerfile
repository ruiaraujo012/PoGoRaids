FROM ubuntu:latest

# WORKDIR /home/app
RUN apt-get update
RUN apt-get -y install curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_11.x  | bash -
RUN apt-get -y install nodejs
RUN npm install -g nodemon
# RUN npm install

# OCR Python
RUN apt-get install python3.7 python3-pip python3-numpy -y
RUN apt-get install tesseract-ocr tesseract-ocr-por -y
RUN pip3 install pytesseract pillow opencv-python datetime numpy

# Project 
COPY package*.json ./
RUN npm install
RUN npm install nodemon -g

COPY . ./

# Change to npm start for deploy
CMD ["npm" , "start"]

