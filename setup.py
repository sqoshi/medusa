from setuptools import find_packages, setup

from beautifiers.welcome import print_welcome


def readfile(filename):
    with open(filename, "r+") as f:
        return f.read()


setup(
    name="medusa",
    version="1.0.0",
    description="Photo editor helpful for ML image preprocessing.",
    long_description=readfile("README.md"),
    url="https://github.com/sqoshi/medusa",
    author="Piotr Popis",
    author_email="piotrpopis@icloud.com",
    license="MIT",
    py_modules=["run"],
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "medusa = run:main",
        ]
    },
    install_requires=[
        "Pillow==8.2.0",
        "termcolor==1.1.0",
    ],
)

print_welcome()
