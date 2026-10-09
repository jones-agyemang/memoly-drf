import os

def cloudflare_mcp_config():
    api_token = None
    return {
        "type": "mcp"
    }
    # return {
        # "type": "mcp",
        # "server_label": "cloudflare_workers_bindings",
        # "server_url": os.getenv(
            # "CLOUDFLARE_MCP_URL",
            # "https://bindings.mcp.cloudflare.com/mcp",
        # ),
        # "headers": {
            # "Authorization": f"Bearer {api_token}",
        # },
        # "require_approval": "never",
    # }