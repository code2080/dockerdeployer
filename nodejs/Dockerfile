FROM timbru31/node-alpine-git

WORKDIR /app

ARG PACKAGES

COPY $PACKAGES /app/package.json

RUN npm i -g serve
RUN npm i -g yarn@latest

RUN yarn install