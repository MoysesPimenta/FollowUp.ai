# syntax=docker/dockerfile:1
FROM node:20-alpine
WORKDIR /app
COPY package.json pnpm-lock.yaml* ./
RUN corepack enable && pnpm install --prod
COPY . .
CMD ["pnpm", "start"]
