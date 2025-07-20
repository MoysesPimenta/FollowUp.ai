FROM node:20-slim
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
COPY backend ./backend
RUN corepack enable && pnpm install --frozen-lockfile --filter @followup/backend...
WORKDIR /app/backend
EXPOSE 3000
CMD ["pnpm", "start"]
