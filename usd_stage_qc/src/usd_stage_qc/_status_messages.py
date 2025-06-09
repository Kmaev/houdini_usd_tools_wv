import hou
def handle_error(message: str):
    """
    Displays an error message if called from inside houdini UI or
    raises the ValueError if called from pipeline scripts
    """
    if hou.isUIAvailable():
        hou.ui.displayMessage(
            text=message,
            buttons=('OK',),
            title="Error",
            severity=hou.severityType.Error
        )
    else:
        hou.puts(f"ERROR: {message}")
    raise ValueError(message)
