from setuptools import setup, find_packages

setup(
    name="dev-assist",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.0",
        "httpx>=0.23.0",  # For async HTTP requests
        "python-dotenv>=1.0.0",
        "rich>=13.0.0",  # For better terminal output
        "typer>=0.9.0",  # For modern CLI interface
    ],
    entry_points={
        'console_scripts': [
            'dev_assist=dev_assist.cli:main',
        ],
    },
    author="Hillary Murefu",
    author_email="hillarywang2005@gmail.com",
    description="A command-line AI assistant for software development",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hillaryhitch/dev_assist",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
