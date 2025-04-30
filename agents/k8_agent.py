import sys, os
from rich import print
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.utils import get_env_vars
from tools.__tool_loader__ import load_tools_config
from prompts.prompt_loader import get_prompt
from core.model import Bedrock
from tools.__tool_executor__ import execute_tools


env_vars = get_env_vars()
tools = load_tools_config(env_vars.get("PLATFORM"))


def call_model(payload):
    llm_call = Bedrock()
    response = llm_call.get_model_response(payload, tools)

    return response

    
     

def run_agent(payload):
    count = 0
    summary = ""
    stop_reason = ""

    while stop_reason != "end_turn":
        count += 1
        print("--------------Thinking---------", count)
        response = call_model(payload)

        ai_message = response["output"]["message"]
        stop_reason = response["stopReason"]

        message_content = response["output"]["message"]["content"]
        payload["message"].append(ai_message)

        for content in message_content:
            if "text" in content:
                summary += content["text"] + "\n"
                print("AI RESPONSE: ", content["text"])

        if stop_reason == "end_turn":
            return message_content[0]["text"]

        if stop_reason == "tool_use":
            tool_results = []
            for content in message_content:
                if "toolUse" not in content:
                    continue

                tool_use = content["toolUse"]
                func_name = tool_use.get("name")
                func_input = tool_use.get("input", {})

                tool_result = {
                    "toolUseId": tool_use["toolUseId"],
                    "status": "",
                    "content": "",
                }
                try:
                    observation, status = execute_tools(func_name, func_input)
                    tool_result["status"] = status
                    tool_result["content"] = [{"text": observation}]
                except Exception as e:
                    tool_result["status"] = status
                    tool_result["content"] = [{"text": f"Some error occurred: {str(e)}"}]

                tool_results.append({"toolResult": tool_result})

            message = {"role": "user", "content": tool_results}
            payload["message"].append(message)

    return message_content[0]["text"]
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-prompt", type=str, default=False, help="enter user prompt")
    args = parser.parse_args()

    if args.user_prompt:
        user_prompt = {"text": args.user_prompt}
    else:
        user_prompt = get_prompt(env_vars.get("USER_PROMPT_PATH"))
    
    system_prompt = get_prompt(env_vars.get("SYSTEM_PROMPT_PATH"))


    payload = {
        "system": [system_prompt],
        "message": [
            {
                "role": "user",
                "content":[user_prompt]
            }
        ]
    }


    summary = run_agent(payload)

    print("\n######### INFORAMTION  ########\n")
    print(summary)
    print("\n######### END  ########\n")