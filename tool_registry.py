from engineering_tools import spindle_speed, feed_rate, cutting_time


tool_registry = {
    "spindle_speed": spindle_speed,
    "feed_rate": feed_rate,
    "cutting_time": cutting_time,
}


def execute_tool(tool_name, arguments):
    if tool_name not in tool_registry:
        raise ValueError(f"Unknown tool: {tool_name}")

    tool = tool_registry[tool_name]

    return tool(**arguments)