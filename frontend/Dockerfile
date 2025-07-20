# Use official Node image
FROM node:20-slim

# Enable corepack so pnpm is available
RUN corepack enable

# Set work directory
WORKDIR /app

# Copy source code
COPY . .

# Install dependencies (none yet, but pnpm expects a lockfile)
RUN pnpm install --frozen-lockfile || true

# Expose port for the UI
EXPOSE 3000

# Serve static files
CMD ["npx", "serve", "./", "-l", "3000"]
