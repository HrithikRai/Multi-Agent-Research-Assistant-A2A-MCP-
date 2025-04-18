from python_a2a import A2AServer, Message, TextContent, MessageRole, run_server

class EchoAgent(A2AServer):

    """A simple agent that will return the message back"""
    def handle_message(self, message):
        if message.content.type == "text":
            return Message(
                content = TextContent(text=f"ECHO: {message.content.text}"),
                role = MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )
        
# Run the server
if __name__ == "__main__":
    agent = EchoAgent()
    run_server(agent, host="0.0.0.0", port=5000)