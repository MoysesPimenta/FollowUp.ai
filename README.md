# FollowUp.ai

This repository hosts the source code and documentation for FollowUp.ai, a WhatsApp CRM.

To understand the system architecture and guidelines, read the [development blueprint](./blueprint.md).

## Project Setup

1. Install [pnpm](https://pnpm.io) if it is not already available:

   ```bash
   curl -fsSL https://get.pnpm.io/install.sh | sh -
   ```

2. Install all workspace dependencies:

   ```bash
   pnpm install
   ```

The repository is organised as a pnpm workspace. Packages are located in the following directories:

- `backend` – server-side services.
- `frontend` – web client.
- `shared` – shared libraries.
- `infra` – infrastructure automation.
- `scripts` – development utilities.

## Running with Docker Compose

Start the backend and frontend containers using:

```bash
docker compose up
```

## Linting and Testing

When linting and test suites are available, run them across the workspace with:

```bash
pnpm lint
pnpm test
```

These commands delegate to each package's `lint` and `test` scripts.

## Contributing

Refer to [`docs/backlog.md`](./docs/backlog.md) for planned work. Please mention the backlog item you are addressing when opening a pull request.
