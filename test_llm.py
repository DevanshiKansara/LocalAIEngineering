from ollama import chat
from engineering_tools import spindle_speed, feed_rate, cutting_time
from tool_registry import tool_registry, execute_tool


messages = [
    {
        "role": "system",
        "content": (
        "You are an engineering calculation assistant. "
        "Use the available Python tools for engineering calculations. "
        "Do not invent, guess, recommend, or silently replace engineering input values. "
        "If a tool reports an error, explain the error and ask the user to provide a valid value. "
        "Do not give example replacement values or example inputs when a tool reports an error. "
        "Only provide engineering recommendations when the user explicitly asks for recommendations."
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
                tool_error = True

                print("\nPython tool error:", error)

                messages.append({
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": f"Tool error: {error}",
                })

                print("\nAI: The engineering calculation could not be completed because the provided input is invalid.")
                print(f"Reason: {error}")
                print("Please provide a valid value.")

        if not tool_error:

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