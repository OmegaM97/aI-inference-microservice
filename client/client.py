import argparse
import grpc
import ai_inference_pb2
import ai_inference_pb2_grpc


def run(host: str, port: int):
    address = f"{host}:{port}"
    with grpc.insecure_channel(address) as channel:
        stub = ai_inference_pb2_grpc.AIInferenceStub(channel)

        print("Testing Sentiment Analysis...")
        response = stub.SentimentAnalysis(
            ai_inference_pb2.SentimentRequest(text="I love this product!")
        )
        print(f"Sentiment: {response.label}, Confidence: {response.confidence}")

        print("\nTesting Real-time LLM Generation...")
        responses = stub.RealTimeLLMGeneration(
            ai_inference_pb2.LLMRequest(prompt="Tell me a joke.")
        )
        full_response = ""
        for response in responses:
            print(response.token, end="")
            full_response += response.token
        print(f"\nFull response: {full_response}")

        print("\nTesting Batch Summarization...")
        def chunk_generator():
            yield ai_inference_pb2.SummarizationChunk(chunk="This is the first part of a long document. ")
            yield ai_inference_pb2.SummarizationChunk(chunk="It contains information about AI. ")
            yield ai_inference_pb2.SummarizationChunk(chunk="The second part discusses machine learning.")

        response = stub.BatchSummarization(chunk_generator())
        print(f"Summary: {response.summary}")

        print("\nTesting Live Chat Assistant...")
        def message_generator():
            yield ai_inference_pb2.ChatMessage(message="Hello")
            yield ai_inference_pb2.ChatMessage(message="How are you?")

        responses = stub.LiveChatAssistant(message_generator())
        print("AI: ", end="", flush=True)
        for response in responses:
            print(response.message, end="", flush=True)
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="AI Inference gRPC client tester.")
    parser.add_argument("--host", default="localhost", help="Load balancer host")
    parser.add_argument("--port", type=int, default=50051, help="Load balancer port")
    args = parser.parse_args()
    run(args.host, args.port)
