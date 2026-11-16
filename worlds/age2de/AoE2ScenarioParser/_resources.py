from importlib.resources import files


def resource(*parts: str):
    return files(__spec__.parent).joinpath(*parts)
