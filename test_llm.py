from ollama import chat
from engineering_tools import spindle_speed, feed_rate
from tool_registry import tool_registry, execute_tool


messages = []

tools = [spindle_speed, feed_rate]


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

            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            print("\nTool requested:", tool_name)
            print("Arguments:", arguments)

            try:
                result = execute_tool(tool_name, arguments)

                print("\nPython calculation:", result)

                messages.append({
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": str(result),
                })

            except ValueError as error:
                print("\nPython tool error:", error)

                messages.append({
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": f"Tool error: {error}",
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