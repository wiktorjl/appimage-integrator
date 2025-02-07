from setuptools import setup, find_packages


with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="pyappimg",
    version="0.1.0",
    author="Wikor Lukasik",
    author_email="pypi@wiktor.io",
    description="A small package to integrate AppImages with the desktop environment",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",
    license="MIT",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
