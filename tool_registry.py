from engineering_tools import spindle_speed, feed_rate


tool_registry = {
    "spindle_speed": spindle_speed,
    "feed_rate": feed_rate,
}


def normalize_arguments(tool_name, arguments):
    if tool_name == "spindle_speed":
        return {
            "cutting_speed": float(arguments["cutting_speed"].replace(" m/min", "")),
            "diameter": float(arguments["diameter"].replace(" mm", "")),
        }

    if tool_name == "feed_rate":
        return {
            "spindle_speed": float(arguments["spindle_speed"]),
            "teeth": int(arguments["teeth"]),
            "feed_per_tooth": float(arguments["feed_per_tooth"]),
        }

    raise ValueError(f"Unknown tool: {tool_name}")


def execute_tool(tool_name, arguments):
    if tool_name not in tool_registry:
        raise ValueError(f"Unknown tool: {tool_name}")

    normalized_arguments = normalize_arguments(tool_name, arguments)

    tool = tool_registry[tool_name]

    return tool(**normalized_arguments)