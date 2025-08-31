'''
The setup.py file is a Python file that contains the necessary information to create a Python package.
It is used to define the metadata and dependencies of the package.
'''
from setuptools import find_packages, setup
from typing import List
from pathlib import Path

def get_requirements() -> List[str]:
    """
    Reads the requirements.txt file and returns a list of dependencies.
    Skips the '-e .' entry used for editable installs.
    """
    requirements: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            # process each line
            for line in file:
                requirement = line.strip()
                #ignore empty lines and -e.
                if requirement and requirement != '-e .':
                    requirements.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found. Please ensure it exists.")
    
    return requirements

# Resolve long description from README either in backend/ or project root
this_dir = Path(__file__).resolve().parent
long_description = ""
for candidate in [this_dir / "README.md", this_dir.parent / "README.md"]:
    if candidate.exists():
        long_description = candidate.read_text(encoding="utf-8")
        break

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Augustine Chibueze",
    author_email="chibuezeaugustine23@gmail.com",
    description="A package for network security-related projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/austinLorenzMccoy/networkSecurity_project",
    packages=find_packages(),
    install_requires=get_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
