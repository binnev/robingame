import glob
import shutil
import subprocess
from pathlib import Path


def cleanup():
    paths = ["dist", "site", ".pytest_cache"]
    paths += glob.glob("*.egg-info")
    paths += glob.glob("*.pytest_cache")
    for path in paths:
        path = Path(__file__).parent / path
        if path.exists():
            shutil.rmtree(path)


def check(question: str):
    response = input(question + " [y/n]: ")
    if response.strip().lower() != "y":
        raise Exception(f"Action required")


def shell(cmd: str):
    try:
        return subprocess.run(
            cmd,
            shell=True,
            check=True,  # raises exception on non-zero returncode
        )
    except subprocess.CalledProcessError:
        raise SystemExit(1)


def announce(s: str):
    print(BOLD)
    print("=" * 80)
    print(s.center(80))
    print("=" * 80)
    print(ENDC, end="")


HEADER = "\033[95m"
OKBLUE = "\033[94m"
OKCYAN = "\033[96m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDC = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

if __name__ == "__main__":
    cleanup()

    announce("Running tests")
    shell("pytest")

    announce("Checking formatting with Black")
    shell("black . --check")

    announce("Checking conventional commits format")
    FIRST_CONVENTIONAL_COMMIT = "1d5afc1e1563836126dba085898dc81bcd344e5b"
    shell(f"cz check --rev-range {FIRST_CONVENTIONAL_COMMIT}..HEAD")

    announce("Bump version and auto-update changelog")
    shell("cz bump")
    check("Does the changelog look OK?")

    announce("Building package")
    shell("python -m build")

    announce("Checking package")
    shell("twine check dist/*")

    announce("PyPI test run")
    shell("twine upload -r pypitest dist/*")
    check(f"Does the testpypi output look OK?")

    announce("PyPI deploy")
    shell("twine upload dist/*")

    announce("Building docs")
    # version import needs to happen after bump
    from robingame import __version__

    shell(f"mike deploy {__version__}")
    shell(f"mike alias {__version__} latest --update-aliases")
    shell("mike list")
    check("Does the list of docs versions look OK?")

    announce("Deploying docs")
    shell(f"mike set-default latest --push")

    cleanup()

    print(f"Finished releasing version {__version__}")
