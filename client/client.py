import grpc
import ai_inference_pb2
import ai_inference_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ai_inference_pb2_grpc.AIInferenceStub(channel)

        # Test 1: Sentiment Analysis
        print("Testing Sentiment Analysis...")
        response = stub.SentimentAnalysis(ai_inference_pb2.SentimentRequest(text="I love this product!"))
        print(f"Sentiment: {response.label}, Confidence: {response.confidence}")

        # Test 2: Real-time LLM Generation
        print("\nTesting Real-time LLM Generation...")
        responses = stub.RealTimeLLMGeneration(ai_inference_pb2.LLMRequest(prompt="Tell me a joke."))
        full_response = ""
        for response in responses:
            print(response.token, end="")
            full_response += response.token
        print(f"\nFull response: {full_response}")

        # Test 3: Batch Summarization
        print("\nTesting Batch Summarization...")
        def chunk_generator():
            yield ai_inference_pb2.SummarizationChunk(chunk="This is the first part of a long document. ")
            yield ai_inference_pb2.SummarizationChunk(chunk="It contains information about AI. ")
            yield ai_inference_pb2.SummarizationChunk(chunk="The second part discusses machine learning.")
        response = stub.BatchSummarization(chunk_generator())
        print(f"Summary: {response.summary}")

        # Test 4: Live Chat Assistant
        print("\nTesting Live Chat Assistant...")
        def message_generator():
            yield ai_inference_pb2.ChatMessage(message="Hello")
            yield ai_inference_pb2.ChatMessage(message="How are you?")
        responses = stub.LiveChatAssistant(message_generator())
        for response in responses:
            print(f"AI: {response.message}", end="")
        print()

if __name__ == '__main__':
    run()