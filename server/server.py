import os
import re
from dotenv import load_dotenv
import grpc
from concurrent import futures
import ai_inference_pb2
import ai_inference_pb2_grpc
from groq import Groq

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')

if api_key and api_key != "12345":
    groq_client = Groq(api_key=api_key)
    use_groq = True
else:
    use_groq = False


class AIInferenceServicer(ai_inference_pb2_grpc.AIInferenceServicer):

    # Unary RPC
    def SentimentAnalysis(self, request, context):
        try:
            if use_groq:
                text = request.text
                prompt = (
                    f"Classify the sentiment of this text: '{text}'. "
                    f"Respond ONLY in this format: POSITIVE 0.95"
                )

                response = groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=50
                )

                result = response.choices[0].message.content.strip()

                match = re.search(r"(POSITIVE|NEGATIVE|NEUTRAL).*?(\d*\.?\d+)", result)

                if match:
                    label = match.group(1)
                    confidence = float(match.group(2))
                else:
                    label, confidence = "NEUTRAL", 0.5

                return ai_inference_pb2.SentimentResponse(
                    label=label,
                    confidence=confidence
                )

            else:
                return ai_inference_pb2.SentimentResponse(
                    label="POSITIVE",
                    confidence=0.9
                )

        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return ai_inference_pb2.SentimentResponse()


    # Server Streaming RPC
    def RealTimeLLMGeneration(self, request, context):
        try:
            if use_groq:
                prompt = request.prompt

                response = groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200,
                    stream=True
                )

                for chunk in response:
                    if not chunk.choices:
                        continue

                    token = chunk.choices[0].delta.content
                    if token:
                        yield ai_inference_pb2.LLMResponse(token=token)

            else:
                mock_response = "This is a mock streaming response from the AI model."
                for token in mock_response.split():
                    yield ai_inference_pb2.LLMResponse(token=token + " ")

        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)


    # Client Streaming RPC
    def BatchSummarization(self, request_iterator, context):
        try:
            aggregated_text = ""

            for chunk in request_iterator:
                aggregated_text += chunk.chunk

            if use_groq:
                prompt = f"Summarize the following text:\n{aggregated_text}"

                response = groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=100
                )

                summary = response.choices[0].message.content.strip()

                return ai_inference_pb2.SummarizationResponse(summary=summary)

            else:
                return ai_inference_pb2.SummarizationResponse(
                    summary=f"Mock summary: {aggregated_text[:50]}..."
                )

        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return ai_inference_pb2.SummarizationResponse()


    # Bidirectional Streaming RPC
    def LiveChatAssistant(self, request_iterator, context):
        try:
            history = []

            for message in request_iterator:
                user_msg = message.message
                history.append({"role": "user", "content": user_msg})

                if use_groq:
                    response = groq_client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=history,
                        max_tokens=100,
                        stream=True
                    )

                    ai_response = ""

                    for chunk in response:
                        if not chunk.choices:
                            continue

                        token = chunk.choices[0].delta.content
                        if token:
                            ai_response += token
                            yield ai_inference_pb2.ChatMessage(message=token)

                    history.append({"role": "assistant", "content": ai_response})

                else:
                    mock_reply = f"Mock AI: I received '{user_msg}'"

                    for token in mock_reply.split():
                        yield ai_inference_pb2.ChatMessage(message=token + " ")

        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    ai_inference_pb2_grpc.add_AIInferenceServicer_to_server(
        AIInferenceServicer(), server
    )

    server.add_insecure_port('0.0.0.0:50051')

    server.start()
    print("Server started on port 50051")

    server.wait_for_termination()


if __name__ == '__main__':
    serve()