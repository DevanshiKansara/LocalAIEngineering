from ollama import chat
from engineering_tools import spindle_speed


messages = []

tools = [spindle_speed]


while True:
    user_input = input("\nYou: ")

    if user_input.lower() in {"exit", "quit"}:
        break

    messages.append({
        "role": "user",
        "content": user_input,
    })

    response = chat(
        model="qwen3:4b",
        messages=messages,
        tools=tools,
    )

    if response.message.tool_calls:
        messages.append(response.message)

        for tool_call in response.message.tool_calls:

            print("\nTool requested:", tool_call.function.name)
            print("Arguments:", tool_call.function.arguments)

            if tool_call.function.name == "spindle_speed":

                diameter = float(
                    tool_call.function.arguments["diameter"].replace(" mm", "")
                )

                cutting_speed = float(
                    tool_call.function.arguments["cutting_speed"].replace(" m/min", "")
                )

                result = spindle_speed(cutting_speed, diameter)

                print("\nPython calculation:", result, "RPM")

                messages.append({
                    "role": "tool",
                    "tool_name": "spindle_speed",
                    "content": str(result),
                })

        final_response = chat(
            model="qwen3:4b",
            messages=messages,
            tools=tools,
        )

        messages.append(final_response.message)

        print("\nAI:", final_response.message.content)

    else:
        messages.append(response.message)

        print("\nAI:", response.message.content)