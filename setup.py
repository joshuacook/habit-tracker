"""Setup configuration for habit-tracker."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="habit-tracker",
    version="0.1.0",
    author="Joshua Cook",
    author_email="joshua@example.com",
    description="A lightweight CLI tool for tracking daily habits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/habit-tracker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
    ],
    python_requires=">=3.12",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "habit=habit.cli:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest==8.0.0",
            "black==24.1.1",
            "ruff==0.2.1",
            "mypy==1.8.0",
        ],
    },
) 