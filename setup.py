from setuptools import setup, find_packages

setup(
    name="seedr_downloader",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "seedr",  # Seedr API package
    ],
    entry_points={
        "console_scripts": [
            "seedr=seedr_downloader.app:main",
        ],
    },
    author="Andrew Phillip Thomasson",
    author_email="drew.thomasson100@gmail.com",
    description="A terminal-based tool for downloading torrents using Seedr.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/seedr_downloader",  # Update with your repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

