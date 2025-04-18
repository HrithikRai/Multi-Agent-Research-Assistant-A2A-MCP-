from python_a2a import A2AServer, run_server, Message,TextContent,MessageRole
from phi.agent import Agent,RunResponse
from phi.tools.googlesearch import GoogleSearch
from phi.model.cohere import CohereChat
from dotenv import load_dotenv
import os
load_dotenv()

cohere_api_key = os.getenv("COHERE_API_KEY")
chat_agent = CohereChat(api_key=cohere_api_key)

def create_search_agent():
    agent = Agent(
        provider=chat_agent,
        tools=[GoogleSearch()],
        description="You are a research assistant who searches the web to find relevant, context rich research material",
        instructions=[
        "Search the web to answer",
        "provide atleast 3 search results",
        "Search in English and make sure to get all relevant references"
    ]
    )
    return agent

class A2ASearchAgent(A2AServer):
    """Phidata based search Agent"""
    def handle_message(self, message):
        if message.content.type == "text":
            agent = create_search_agent()
            response = agent.run(message.content.text)           
            return Message(
                content = TextContent(text=response.content),
                role = MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )
        
if __name__ == "__main__":
    agent = A2ASearchAgent()
    run_server(agent, host="0.0.0.0", port=5002)

