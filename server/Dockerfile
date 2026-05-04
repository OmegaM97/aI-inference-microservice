FROM python:3.14-slim

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir groq grpcio protobuf python-dotenv

COPY server/server.py ./
COPY server/ai_inference_pb2.py ./
COPY server/ai_inference_pb2_grpc.py ./

EXPOSE 50051

CMD ["python", "server.py"]
