from python_a2a import A2AServer, run_server, Message,TextContent,MessageRole
import cohere
from dotenv import load_dotenv
import os
load_dotenv()

cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere.ClientV2(cohere_api_key)

system_message="""
## Task and Context
You are an helpful research assistant whose job is to summarize.

## Style Guide
Speak in a professional academic tone."""

class A2ASummarizer(A2AServer):
    """Cohere based Info Summarizer"""
    def handle_message(self, message):

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
        
if __name__ == "__main__":
    agent = A2ASummarizer()
    run_server(agent, host="0.0.0.0", port=5003)

