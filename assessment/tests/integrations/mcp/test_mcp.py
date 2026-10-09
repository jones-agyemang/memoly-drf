from integrations.cloudflare.mcp import cloudflare_mcp_config

def describe_mcp_configuration():

    def it_returns_valid_config():
        expected_valid_config = cloudflare_mcp_config()

        assert expected_valid_config.keys