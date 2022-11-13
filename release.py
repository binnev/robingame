import shutil
import subprocess
from pathlib import Path


def cleanup():
    for folder in [Path(__file__).parent / "robingame.egg-info", Path(__file__).parent / "dist"]:
        if folder.exists():
            shutil.rmtree(folder)


if __name__ == '__main__':
    cleanup()
    subprocess.run("python -m build".split())
    subprocess.run("twine upload dist/*".split())
    cleanup()
