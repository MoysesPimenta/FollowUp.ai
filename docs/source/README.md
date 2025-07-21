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

Build and start both the API and UI containers:

```bash
docker compose up --build
```

The API will be available on `http://localhost:8000` and the UI on `http://localhost:3000`.

## Linting and Testing

When linting and test suites are available, run them across the workspace with:

```bash
pnpm lint
pnpm test
```

These commands delegate to each package's `lint` and `test` scripts.

## Building Documentation

Build the HTML documentation locally with Sphinx:

```bash
cd docs
make -C source html
```

The generated site can be found in `docs/source/_build/html`.

## Contributing

Refer to [`backlog.md`](backlog.md) for planned work. Please mention the backlog item you are addressing when opening a pull request.
