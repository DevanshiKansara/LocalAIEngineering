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

    print("\nAI:", response.message.content)

    print("\nTool calls:", response.message.tool_calls)

    messages.append(response.message)