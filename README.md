# AI Inference Microservice

This is a gRPC-based AI Inference microservice using Protocol Buffers for API contracts. It implements four types of RPCs: Unary, Server-Streaming, Client-Streaming, and Bidirectional-Streaming.

## Features

- **Sentiment Analysis**: Unary RPC to classify text sentiment.
- **Real-time LLM Generation**: Server-Streaming RPC for token-by-token text generation.
- **Batch Summarization**: Client-Streaming RPC to summarize large texts.
- **Live Chat Assistant**: Bidirectional-Streaming RPC for conversational AI.

## Setup

1. Install dependencies:
   ```
   pip install grpcio grpcio-tools protobuf groq python-dotenv
   ```

2. Set your Groq API key in `.env`:
   ```
   GROQ_API_KEY=your_actual_api_key_here
   ```

3. Generate gRPC stubs (already done):
   ```
   python -m grpc_tools.protoc --proto_path=protos --python_out=. --grpc_python_out=. protos/ai_inference.proto
   ```

## Running locally

1. Start the server:
   ```
   python server/server.py
   ```

2. Run the client against the load balancer:
   ```
   python client/client.py --host localhost --port 50051
   ```

## Docker + Load Balancer

1. Build and start the mesh:
   ```
   docker compose up --build
   ```

2. Run the client against Nginx load balancer:
   ```
   python client/client.py --host localhost --port 50051
   ```

The Nginx load balancer listens on port `50051` and distributes gRPC requests round robin across three backend replicas.

If no valid API key is provided, the server runs in mock mode for testing.

## Project Structure

- `protos/`: Protocol Buffer definitions
- `server/`: gRPC server implementation
- `client/`: gRPC client for testing
- `nginx/`: (For future reverse proxy setup)
- `.env`: Environment variables (API key)