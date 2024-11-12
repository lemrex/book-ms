# Stage 1: Build
FROM node:18-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm install --only=production

COPY . .

# Stage 2: Productions
FROM node:18-alpine

WORKDIR /app
COPY --from=build /app /app

EXPOSE 3000
CMD ["node", "src/app.js"]
