FROM node:22-alpine

WORKDIR /app

COPY package.json .
COPY package*.json .

RUN npm install
RUN npm i -g serve

COPY . .

# DECLARE YOUR BUILD ARGS HERE
# (Replace with your actual variable names, e.g., REACT_APP_API_URL or VITE_API_URL)
# ARG FRONTEND_API_URL
# ENV FRONTEND_API_URL=$FRONTEND_API_URL

RUN npm run build

EXPOSE 3000

CMD [ "serve", "-s", "dist" ]