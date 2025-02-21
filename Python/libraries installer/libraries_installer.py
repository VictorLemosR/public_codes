import subprocess
import sys


def main():
    PACKAGES_REQUIREMENTS = {
        "ipython": "",
        "polars": "",
        "pandas": "",
        "xlwings": "",
        "openpyxl": "",
        "xlsxwriter": "",
        "sqlalchemy": "",
        "pyodbc": "",
        "pyarrow": "",
        "neovim": "pynvim",
        "fastexcel": "",
        "selenium": "",
        "requests": "",
        "connectorx":"",
        "holidays": "",
        "pypdf": "",

    }

    pkg_resources = import_pkg_resources()

    installed_packages = get_installed_packages(pkg_resources)

    missing_packages = check_missing_packages(PACKAGES_REQUIREMENTS, installed_packages)

    update_pip_function()
    update_installed_libraries(installed_packages)
    install_missing_libraries(missing_packages)

    print(f"\n\n\n\nLibraries installed:\n{missing_packages}")


def import_pkg_resources():
    try:
        import pkg_resources
    except ImportError:
        python = sys.executable
        subprocess.check_call(
            [python, "-m", "pip", "install", "setuptools"], stdout=subprocess.DEVNULL
        )
        import pkg_resources
    return pkg_resources


def get_installed_packages(pkg_resources):
    pkg_resources = import_pkg_resources()
    installed_packages = []
    for pkg in pkg_resources.working_set:
        print(f"pkg: {pkg.key}")
        installed_packages.append(pkg.key)

    return installed_packages


def check_missing_packages(PACKAGES_REQUIREMENTS, installed_packages):
    packages_install = {}
    for package in PACKAGES_REQUIREMENTS.keys():
        if package not in installed_packages:
            pip_name = PACKAGES_REQUIREMENTS[package]
            if pip_name == "":
                pip_name = package
            packages_install[package] = pip_name
    missing = packages_install.values()

    return missing


def update_pip_function():
    # Update pip
    print("Checking if 'pip' is on last version")
    python = sys.executable
    subprocess.check_call(
        [python, "-m", "pip", "install", "--upgrade", "pip"],
        stdout=subprocess.DEVNULL,
    )


def update_installed_libraries(installed_packages):
    # Update current libraries
    for package in installed_packages:
        print(f"Checking update of: {package}")
        python = sys.executable
        # subprocess.check_call([python, "-m", "pip", "install", package, "--upgrade"])
        subprocess.check_call(
            [python, "-m", "pip", "install", package, "--upgrade"],
            stdout=subprocess.DEVNULL,
        )  # Hide pip install lines


def install_missing_libraries(missing):
    # Install required libraries
    if missing:
        python = sys.executable
        # subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL) #Hide pip install lines
        subprocess.check_call([python, "-m", "pip", "install", *missing])


if __name__ == "__main__":
    main()
