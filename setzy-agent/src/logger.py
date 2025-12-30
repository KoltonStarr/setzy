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