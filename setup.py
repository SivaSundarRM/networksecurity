from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    """ This function reads the requirements from a given file and returns them as a list. """
    
    requirements = []
    try:
        with open(file_path) as file:
            requirements = file.readlines()
            requirements = [req.strip() for req in requirements]

            if HYPHEN_E_DOT in requirements:
                requirements.remove(HYPHEN_E_DOT)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"An error occurred while reading {file_path}: {e}")
        return []
    return requirements
setup(
    name="mlproject",
    version="0.1",
    author="Siva",
    author_email="sivaramachandran143@gmail.com", 
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
    )
print(get_requirements('requirements.txt'))