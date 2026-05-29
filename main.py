from fastmcp import FastMCP
import random
import json

# Create the fasmsp server instance
mcp = FastMCP("Simple Calculatoer server")

@mcp.tool
def add(a:int , b:int) -> int:
    """ADD two numbers together.
    args:
        a: First number
        b: second number

    Returns:
        The sum of two number
    """

    return a + b


# Generate random number
@mcp.tool
def random_number(min_value: int = 1, max_value: int = 100)-> int:
    """Generate a random umber within a range 

    args:
        min_Value: minimum value (default: 1)
        max_Value: maximum value (default: 100)

    returns: 
        A random integer between min_value and max_value
    """
    return random.randint(min_value, max_value)

#Resource Server information
@mcp.resource("info://server")
def server_info()-> str:
    """Get information about this server"""
    info = {
        "name": "Simple Calculator Server",
        "version" : "1.0.0",
        "description": "A basic MCP server with ath tools",
        "tools": ["add", "random_number"],
        "author": "your Name"
    }
    return json.dumps(info, indent=2)

# Start Server


if __name__ == "__main__":
    mcp.run(transport="http", host= "0.0.0.0", port=8000) #major change

# to run == uv run main.py
# to inspect == uv run fastmcp dev inspector main.py