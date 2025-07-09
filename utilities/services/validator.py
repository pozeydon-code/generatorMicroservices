def pluralize(name: str) -> str:
    if name.endswith("y"):
        # quita la 'y' y añade 'ies'
        return name[:-1] + "ies"
    else:
        return name + "s"
