from python_a2a import A2AServer, run_server, Message,TextContent,MessageRole,FunctionResponseContent
import cohere, requests, os
from dotenv import load_dotenv
load_dotenv()

cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere.ClientV2(cohere_api_key)

system_message="""
## Task and Context
You are an helful assistant who assists scholars with their research.

## Style Guide
Speak in a professional academic tone."""

def get_current_location():
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        city= data.get("city", "Unknown"),
        
        return f"city {city[0]}"

class A2ACohereServer(A2AServer):
    """Cohere based LLM Agent"""
    def handle_message(self, message):
        if message.content.type == "text":
            messages = [{'role': 'system', 'content': system_message},
            {'role': 'user', 'content': message.content.text}]

            response = co.chat(model="command-r-plus-08-2024",
                    messages=messages).message.content[0].text
            
            return Message(
                content= TextContent(
                    text = f"{response}"
                ),
                role = MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )
        
        elif message.content.type == "function_call":
            function_name = message.content.name            
            try:
                if function_name == "get_location":         
                    return Message(
                        content=FunctionResponseContent(
                            name="get_location",
                            response={"Hello Researcher from city :": get_current_location()}
                        ),
                        role=MessageRole.AGENT
                    )
            except Exception as e:
                return Message(
                    content=FunctionResponseContent(
                        name=function_name,
                        response={"error": str(e)}
                    ),
                    role=MessageRole.AGENT,
                    parent_message_id=message.message_id,
                    conversation_id=message.conversation_id
                )
        
if __name__ == "__main__":
    agent = A2ACohereServer()
    run_server(agent, host="0.0.0.0", port=5001)

