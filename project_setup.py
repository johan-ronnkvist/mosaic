import subprocess
import sys


def poetry_installed() -> bool:
    try:
        subprocess.run(["poetry", "--version"], check=True, stdout=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_dependencies() -> None:
    print(" - Installing dependencies...")
    subprocess.run(["poetry", "install"], check=True)


def install_git_hooks() -> None:
    print(" - Installing git hooks...")
    subprocess.run(["poetry", "run", "pre-commit", "install"], check=True)


def main() -> int:
    print("Setting up project...")
    if not poetry_installed():
        print(" - Poetry is not installed. Please install poetry first.")
        return 1

    install_dependencies()
    install_git_hooks()

    return 0


if __name__ == "__main__":
    sys.exit(main())
