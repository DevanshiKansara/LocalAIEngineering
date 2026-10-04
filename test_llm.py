from ollama import chat
from engineering_tools import spindle_speed, feed_rate, cutting_time
from tool_registry import tool_registry, execute_tool

print("=" * 60)
print("        Local AI Engineering Assistant")
print("=" * 60)

messages = [
    {
        "role": "system",
        "content": (
            "You are an engineering calculation assistant. "
            "For every engineering calculation, you MUST use the appropriate Python tool. "
            "Never perform an engineering calculation or validation yourself when a Python tool is available. "
            "Do not invent, guess, recommend, or silently replace engineering input values. "
            "If a tool reports an error, explain the error and ask the user to provide a valid value. "
            "Do not give example replacement values or example inputs when a tool reports an error. "
            "Only provide engineering recommendations when the user explicitly asks for recommendations. "
            "Only state conclusions that are directly supported by the tool results. "
            "Do not comment on whether calculated values are typical, safe, optimal, appropriate, efficient, or suitable "
            "unless the user explicitly asks for an evaluation or recommendation. "
            "When a requested calculation is complete, provide the result and a concise calculation summary."
        ),
    }
]


tools = [spindle_speed, feed_rate, cutting_time]


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
        options={"temperature": 0},
    )

    if response.message.tool_calls:
        messages.append(response.message)

        tool_error = False

        for tool_call in response.message.tool_calls:

            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            print(f"\n[Tool] {tool_name}")

            try:
                result = execute_tool(tool_name, arguments)

                if tool_name == "spindle_speed":
                    print(f"      → {result:.2f} RPM")
                elif tool_name == "feed_rate":
                    print(f"      → {result:.2f} mm/min")
                elif tool_name == "cutting_time":
                    print(f"      → {result:.4f} min")

                messages.append({
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": str(result),
                })

            except ValueError as error:

                tool_error = True

                print("\nPython tool error:", error)

                print(
                    "\nAI: The engineering calculation could not be "
                    "completed because the provided input is invalid."
                )
                print(f"Reason: {error}")
                print("Please provide a valid value.")

                break

        if not tool_error:

            while True:

                next_response = chat(
                    model="qwen3:4b",
                    messages=messages,
                    tools=tools,
                    options={"temperature": 0},
                )

                messages.append(next_response.message)

                if not next_response.message.tool_calls:

                    print("\nAI:", next_response.message.content)
                    break

                for tool_call in next_response.message.tool_calls:

                    tool_name = tool_call.function.name
                    arguments = tool_call.function.arguments

                    print(f"\n[Tool] {tool_name}")

                    try:
                        result = execute_tool(tool_name, arguments)

                        if tool_name == "spindle_speed":
                            print(f"      → {result:.2f} RPM")
                        elif tool_name == "feed_rate":
                            print(f"      → {result:.2f} mm/min")
                        elif tool_name == "cutting_time":
                            print(f"      → {result:.4f} min")

                        messages.append({
                            "role": "tool",
                            "tool_name": tool_name,
                            "content": str(result),
                        })

                    except ValueError as error:

                        tool_error = True

                        print("\nPython tool error:", error)

                        print(
                            "\nAI: The engineering calculation could not be "
                            "completed because the provided input is invalid."
                        )
                        print(f"Reason: {error}")
                        print("Please provide a valid value.")

                        break

                if tool_error:
                    break

    else:
        messages.append(response.message)

        print("\nAI:", response.message.content)
