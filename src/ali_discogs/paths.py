import os


def repo_root() -> str:
    env = os.environ.get("ALI_DISCOGS_ROOT")
    if env:
        return os.path.abspath(env)
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(os.path.dirname(here))
    if os.path.isdir(os.path.join(root, "raw")):
        return root
    cwd = os.getcwd()
    if os.path.isdir(os.path.join(cwd, "raw")):
        return cwd
    return root


def raw_dir() -> str:
    return os.path.join(repo_root(), "raw")


def data_dir() -> str:
    return os.path.join(repo_root(), "data")
