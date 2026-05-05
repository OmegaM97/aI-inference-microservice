# AI Inference Microservice

A lightweight gRPC microservice demo that runs three identical AI inference servers behind an Nginx gRPC load balancer.

## Overview

This repository demonstrates a Dockerized microservice architecture for AI inference:
- `server/`: gRPC server implementation with multiple RPC styles
- `nginx/`: Nginx configuration acting as a gRPC load balancer
- `client/`: Python client to test the available inference endpoints
- `docker-compose.yml`: brings up 3 server containers plus the Nginx load balancer on a shared Docker network

## Features

- Unary RPC: sentiment analysis
- Server streaming RPC: real-time LLM generation
- Client streaming RPC: batch summarization
- Bidirectional streaming RPC: live chat assistant
- Load-balanced gRPC routing through Nginx
- Optional Groq API integration via `GROQ_API_KEY`

## Architecture

1. `client/client.py` connects to the Nginx load balancer at `localhost:50051`
2. `nginx` accepts gRPC on port `50051` and forwards traffic to:
   - `server1:50051`
   - `server2:50051`
   - `server3:50051`
3. Each server runs the same AI inference code and supports the same gRPC service API
4. Services are connected via the Docker network `ai_mesh`

## Prerequisites

- Docker
- Docker Compose
- Python 3.14+
- `uv` package manager installed globally or available in your environment

## Install dependencies

From the project root, install Python dependencies using `uv`:

```bash
uv sync
```

If `uv` is not installed yet, install it first with:

```bash
python -m pip install uv
```

## Run the project with Docker Compose

Build and start all containers using:

```bash
docker-compose up --build
```

This command does the following:
- builds the server image from `server/Dockerfile`
- starts three server containers: `ai_server_1`, `ai_server_2`, `ai_server_3`
- starts the Nginx load balancer container: `ai_nginx`
- connects all containers on the `ai_mesh` Docker bridge network

## Test the microservice

With Docker Compose running, run the test client from the project root:

```bash
python client/client.py --host localhost --port 50051
```

That client performs:
- Sentiment analysis
- Real-time LLM generation streaming
- Batch summarization using client streaming
- Live chat assistant using bidirectional streaming

## Optional environment configuration

Create a `.env` file in the project root to provide a Groq API key:

```env
GROQ_API_KEY=your_real_api_key_here
```

If `GROQ_API_KEY` is missing or set to `12345`, the server returns mock responses instead of calling the Groq API.

## Notes

- The `server/Dockerfile` exposes port `50051` and starts the Python gRPC server.
- Nginx is configured for HTTP/2 gRPC pass-through in `nginx/nginx.conf`.
- The load balancer ensures traffic is distributed across three service instances.

## Quick commands

```bash
uv sync

docker-compose up --build
python client/client.py --host localhost --port 50051
```

## Project files

- `docker-compose.yml` — service orchestration for servers and Nginx
- `nginx/nginx.conf` — gRPC load balancer configuration
- `server/server.py` — AI inference gRPC server implementation
- `client/client.py` — test client for all RPC methods
- `pyproject.toml` — project metadata and dependencies
