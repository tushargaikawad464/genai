
import os
import yaml


def load_tools_config(platform):
    script_path = os.path.dirname(os.path.realpath(__file__))

    file_path = f"{script_path}/tools.yaml"
    with open(file_path) as f:
        raw_config = yaml.safe_load(f)

    tools = []

    print("Loading Agent Tooling Skills:")

    if not raw_config.get("tools", []):
        raise ValueError("No Agent Tooling Skills Found")

    for tool in raw_config.get("tools", []):
        data = generate_platform_schema(platform, tool)
        tools.append(data)

    print("Agent Skills Loaded Successfully.")
    return tools


def generate_platform_schema(platform, tool):
    if platform == "OpenAI":
        return {
            "name": tool.get("name"),
            "type": "function",
            "description": tool.get("description"),
            "parameters": {
                "type": "object",
                "properties": tool.get("parameters", {}),
                "required": tool.get("required", []),
            },
        }
    elif platform == "Bedrock":
        return {
            "toolSpec": {
                "name": tool.get("name"),
                "description": tool.get("description"),
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": tool.get("parameters", {}),
                        "required": tool.get("required", []),
                    }
                },
            }
        }
    else:
        raise ValueError(f"Unsupported platform: {platform}")
