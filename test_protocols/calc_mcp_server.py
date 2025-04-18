# MCP server that exposes mathematical operations as standardized tools

from python_a2a.mcp import FastMCP, text_response

# Create a new MCP server
calculator_mcp = FastMCP(
    name="Calculator MCP",
    version="1.0.0",
    description="Provides mathematical calculation functions"
)
# Define tools using simple decorators with type hints
@calculator_mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b
@calculator_mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b
@calculator_mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b
@calculator_mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        return text_response("Cannot divide by zero")
    return a / b
# Run the server
if __name__ == "__main__":
    calculator_mcp.run(host="0.0.0.0", port=5000)