"""Setup configuration for TODO Project."""

from setuptools import setup, find_packages

setup(
    name="todo-project",
    version="1.0.0",
    author="TODO Team",
    description="TODO management app with shared components",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "python-dotenv>=0.19.0",
    ],
)
