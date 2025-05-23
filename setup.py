from setuptools import setup, find_packages

setup(
    name="trunk-cli",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'trunk = trunk.cli:main',
        ],
    },
    author="Your Name",
    description="A simple directory tree visualizer",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Utilities"
    ],
    python_requires=">=3.7",
)
