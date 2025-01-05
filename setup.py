'''
The setup.py file is a Python file that contains the necessary information to create a Python package.
It is used to define the metadata and dependencies of the package.
'''
from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    Reads the requirements.txt file and returns a list of dependencies.
    Skips the '-e .' entry used for editable installs.
    """
    requirements: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            for line in file:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirements.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found. Please ensure it exists.")
    
    return requirements

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Augustine Chibueze",
    author_email="chibuezeaugustine23@gmail.com",
    description="A package for network security-related projects.",
    long_description=open("README.md").read(),
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
