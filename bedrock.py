import boto3
from utils import get_env_vars

env_vars = get_env_vars()


class Bedrock:
    def __init__(self):
        self.REGION = env_vars.get("REGION")
        self.MODEL_ID = env_vars.get("MODEL_ID")
        self.bedrock_client = boto3.client("bedrock-runtime", region_name=self.REGION)

    def get_model_response(self, payload, tools):
        if tools:
            response = self.bedrock_client.converse(
                system=payload["system"],
                messages=payload["message"],
                toolConfig={"tools": tools},
                modelId=self.MODEL_ID,
            )
            return response
        else:
            response = self.bedrock_client.converse(
                system=payload["system"],
                messages=payload["message"],
                modelId=self.MODEL_ID
            )

            return response
