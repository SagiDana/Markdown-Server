import os
from setuptools import setup, find_packages

setup(
    name="markdown-server",
    version="0.0.1",
    description="A simple markdown server.",
    classifiers=[],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[  "Flask", 
                        "Markdown",
                        "py-gfm"],
    entry_points={
        "console_scripts": [
            "markdownserver=markdownserver:main",
        ]
    },
)
