from langchain.messages import ToolMessage, AIMessage, HumanMessage

def log(message: str, color: str = "white") -> None:
    """Print colored text to the terminal.
    
    Args:
        message: The text to print
        color: Color name (red, green, yellow, blue, magenta, cyan, white)
    """
    colors = {
        "red": "\033[1m\033[91m",
        "green": "\033[1m\033[92m",
        "yellow": "\033[1m\033[93m",
        "blue": "\033[1m\033[94m",
        "magenta": "\033[1m\033[95m",
        "cyan": "\033[1m\033[96m",
        "white": "\033[1m\033[97m",
    }
    
    reset = "\033[0m"
    color_code = colors.get(color.lower(), colors["white"])
    print(f"{color_code}{message}{reset}")

def log_agent_msg(msg: ToolMessage | AIMessage | HumanMessage) -> None: 
    match msg.type:
        case "human":
            log("================================ 👤 Human Message 👤 =================================")
            log(msg.content)
        case "ai":
            log("================================== 🤖 Ai Message 🤖 ==================================", "blue")
            if msg.content:
                log(msg.content, "blue")
            else:
                log("I need to use a tool.", "blue")
        case "tool":
            log("================================== 🛠️ Tool Message 🛠️ ==================================", "yellow")
            tool_call = msg.to_json()["kwargs"]
            log("Name: " + tool_call["name"], "yellow")
            log("Status: " + tool_call["status"], "yellow")
        case _:
            log("Unknown MSG type.")