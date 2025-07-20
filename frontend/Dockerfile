FROM node:20-slim
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
COPY frontend ./frontend
RUN corepack enable && pnpm install --frozen-lockfile --filter @followup/frontend...
WORKDIR /app/frontend
EXPOSE 3000
CMD ["pnpm", "start"]
