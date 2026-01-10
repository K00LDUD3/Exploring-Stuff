def CheckFlag(file_name : str = "Flag.txt"):
    lines = []
    with open(file_name, 'r') as f:
        lines = f.readlines()

    if len(lines) == 0:
        return 0
    return 1


# print(CheckFlag("Flag.txt"))