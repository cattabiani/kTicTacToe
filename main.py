from kTicTacToe import commands

cmd = ""
ext = {"exit", "e"}
available_commands = [
    func
    for func in dir(commands)
    if callable(getattr(commands, func)) and not func.startswith("__")
]

while cmd not in ext:
    cmd = input("next command (e/exit to exit)")
    cmd = cmd.split()
    args = cmd[1:]
    cmd = cmd[0]
    if cmd in ext:
        continue

    try:
        getattr(commands)(*args)
    except AttributeError:
        print(
            f"command {cmd} not found! Possible options: {', '.join(available_commands)}"
        )
