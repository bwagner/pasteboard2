#!/usr/bin/env python

import runpy
import shutil
from pathlib import Path

import requests
import tomlkit


def delete_dir(path: Path):
    if not path:
        print(f"Error: '{path}' invalid.")
        return False
    if not path.is_dir():
        print(f"Error: '{path}' not a dir.")
        return False
    stat = path.stat()
    if not stat:
        print(f"Error: can't read '{path}'.")
        return False
    # Try to remove the tree; if it fails, throw an error using try...except.
    try:
        shutil.rmtree(path)
        return True
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}.")

    return False


def setup_dist_dir():
    path = Path("dist")
    if not delete_dir(path):
        print(f"deleting '{path}' failed, exiting.")
        return
    Path.mkdir(path)


def build():
    runpy.run_module(mod_name="build", run_name="__main__", alter_sys=True)


def get_pypi_version(package_name):
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        response.raise_for_status()
        data = response.json()
        return data["info"]["version"]
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            return "0.0.1"
        else:
            print(f"HTTP Error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Error Connecting")
    except requests.exceptions.Timeout:
        print("Timeout Error")
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")


def bump_version(version_str, bump_flags=1):
    """
    Bump the version string based on the given flags.

    Args:
        version_str (str): A string in the format 'x.x.x'.
        bump_flags (int): An integer that is an OR'ed combination of:
            4: Bump the major version.
            2: Bump the minor version.
            1: Bump the patch version (default).

    Returns:
        str: The bumped version string.
    """

    major, minor, patch = map(int, version_str.split("."))

    if bump_flags & 4:  # Major
        major += 1
        minor, patch = 0, 0  # Reset minor and patch
    elif bump_flags & 2:  # Minor
        minor += 1
        patch = 0  # Reset patch
    elif bump_flags & 1:  # Patch
        patch += 1

    return f"{major}.{minor}.{patch}"


def set_version_in_pyproject(version_str, filepath="pyproject.toml"):
    """
    Set the version in the pyproject.toml file to a given value.

    Args:
        version_str (str): The new version string.
        filepath (str): The path to the pyproject.toml file.
            Defaults to 'pyproject.toml'.

    Returns:
        None
    """

    try:
        with open(filepath, "r") as file:
            pyproject = tomlkit.load(file)

        pyproject["project"]["version"] = version_str

        with open(filepath, "w") as file:
            tomlkit.dump(pyproject, file)
    except FileNotFoundError:
        print(f"{filepath} not found.")
    except KeyError:
        print("Key not found in the file.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    dist_dir = "dist"
    print(f"setting up {dist_dir} directory")
    setup_dist_dir()
    package = Path.cwd().name
    print(f"getting current version number on pypi for {package}: ", end="")
    pypi_version = get_pypi_version(package)
    print(pypi_version)
    next_version = bump_version(pypi_version)
    print(f"setting version to {next_version} for {package} in {dist_dir}")
    set_version_in_pyproject(next_version)
    print(f"building {package}")
    build()
    dist = Path("dist")
    wheel = str(next(dist.glob("*.whl")))
    print(
        "now test by (creating) activating a virtual env\n"
        f"pip uninstall {package}\n"
        f"pip install {wheel}\n"
        f"test the package {package} interactively\n"
        f"pip uninstall {package}\n"
        "deactivate\n"
        "if you're happy:\n"
        "python -m twine upload dist/*\n"
    )


if __name__ == "__main__":
    main()
