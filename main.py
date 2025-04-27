from bedrock import Bedrock
from generate_tools import load_tools_config
from utils import get_env_vars
from knowledge_base import execute_tools
from rich import print

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
        print("RESPONSE \n", response)

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
                    "status": "success",
                    "content": "",
                }
                try:
                    observation = execute_tools(func_name, func_input)
                    tool_result["content"] = [{"text": observation}]
                except Exception as e:
                    tool_result["status"] = "failure"
                    tool_result["content"] = [{"text": f"Some error occurred: {str(e)}"}]

                tool_results.append({"toolResult": tool_result})

            message = {"role": "user", "content": tool_results}
            payload["message"].append(message)
            print("payload: \n", payload)
    return message_content[0]["text"]
                
if __name__ == "__main__":
    payload = {
        "system": [{"text": "you are an ai assisant who ans only k8 releated questions, make your ans short and crisp"}],
        "message": [
            {
                "role": "user",
                "content":[
                    {
                        "text": "what is the name of cluster running in my local, and how many namespace and pods are there"
                    }
                ]
            }
        ]
    }
    summary = run_agent(payload)

    print("\n######### INFORAMTION  ########\n")
    print(summary)
    print("\n######### END  ########\n")