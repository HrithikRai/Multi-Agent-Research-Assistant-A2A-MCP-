from python_a2a import A2AClient, Message, TextContent, MessageRole

# Create a client , send a message, get response
client = A2AClient("http://localhost:5004/a2a")
message = Message(
    content=TextContent(text="Hey there, what is 4+5?"),
    role=MessageRole.USER
)
response = client.send_message(message)
print(f"Agent says: {response.content.text}")