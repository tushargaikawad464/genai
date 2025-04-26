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
    count=0
    summery=""
    stop_reason=""

    while stop_reason != "end_turn":
        count +=1
        print("--------------Thinking---------", count)
        response =  call_model(payload)

        ai_message = response["output"]["message"]
        stop_reason = response["stopReason"]

        messasge_content = response["output"]["message"]["content"]
        payload["message"].append(ai_message)

        for content in messasge_content:
            if "text" in content:
                summery += content["text"] + "\n"
                print("AI RESPONSE: ", content["text"])

        if stop_reason == "end_turn":
            return messasge_content[0]["text"]
            break

        elif stop_reason == "tool_use":
            action_dict = next(
                (item for item in messasge_content if "toolUse" in item), None
            )

            if action_dict is None:
                payload["message"].append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": "Oberservation: No action has been performed, Finish your goal using tools available to you"
                            }
                        ]
                    }
                )
                continue
            
            tool_use = action_dict["toolUse"]
            func_name = tool_use.get("name")
            func_input = tool_use.get("input", {})


            tool_result = {
                "toolUseId": tool_use["toolUseId"],
                "status": "success",
                "content": "",
            }


            try:
                oberservation = execute_tools(func_name, func_input)
                tool_result["content"] = [{"text": oberservation}]

            except Exception as e:
                tool_result["content"] = [{"text": f"Some error occcured: {str(e)}"}]

            message = {"role": "user", "content": [{"toolResult": tool_result}]}
            payload["message"].append(message)

    return messasge_content[0]["text"]

if __name__ == "__main__":
    payload = {
        "system": [{"text": "you are an ai assisant who ans only k8 releated questions"}],
        "message": [
            {
                "role": "user",
                "content":[
                    {
                        "text": "what is the name of cluster running in my local,"
                    }
                ]
            }
        ]
    }
    summary = run_agent(payload)

    print("\n######### INFORAMTION  ########\n")
    print(summary)
    print("\n######### END  ########\n")