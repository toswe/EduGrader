FROM node:22.11.0

WORKDIR /frontend

COPY . .

RUN npm install

# TODO Build the react app and serve staic files
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
