# One-time setup so MCP can start its background server inside Jupyter.
# It simply points the server's logs at a normal file (mcp_server.log).
import mcp.client.stdio
mcp.client.stdio.stdio_client.__wrapped__.__defaults__ = (open("mcp_server.log", "w"),)
print("MCP setup done")