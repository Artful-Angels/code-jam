# BugSweeper Frontend

The frontend for BugSweeper uses Vue and is written in TypeScript. For development, it can be run manually, or using docker.

## Using Docker

**Note: it's currently not possible to get hot-reloads for development using docker. For that reason, I'd recommend following the [manual installation](#manual-installation) if you're working on the frontend.**


Build and run the docker container using compose:

```sh
docker-compose up --build
```

Alternatively, you can run the commands separately:

```sh
docker-compose build
docker-compose up
```

## Manual Installation

```sh
npm install
```

Compile and Hot-Reload for Development. This is currently not possible using Docker.

```sh
npm run dev
```

### Linting

```sh
npm run lint
```
