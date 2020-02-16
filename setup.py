#!/usr/bin/env python3

from setuptools import setup, find_packages

REPOSITORY:str = "https://www.github.com/cosasdepuma/mrrobot"

def readme() -> str:
    with open("README.md","r") as README:
        return README.read()

def requirements() -> list:
    with open("requirements.txt","r") as dependencies:
        return dependencies.readlines()

setup(
    name='mrrobot',
    version='1.0.0',
    description='Just another robot to automate the hacking process',
    long_description=readme(),
    long_description_content_type="text/markdown",
    license="GPL-3.0",
    keywords="mrrobot elliot hacking ctf flag",
    author='Kike Fontan (@CosasDePuma)',
    author_email='kikefontanlorenzo@gmail.com',
    url="https://fsundays.tech/",
    project_urls={
        "Bug Tracker": f"{REPOSITORY}/issues",
        "Documentation": REPOSITORY,
        "Source Code": REPOSITORY
    },
    packages=find_packages(),
    zip_safe=True,
    install_requires=requirements(),
    python_requires=">=3.8",
    platforms=["any"],
    entry_points={ 'console_scripts': ['mrrobot=mrrobot:entrypoint'] },
    classifiers=[   
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: Free For Educational Use",
        "License :: Free for non-commercial use",
        "License :: Free To Use But Restricted",
        "Natural Language :: English",
        "Natural Language :: Spanish",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Documentation",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Education",
        "Topic :: Education :: Testing",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Puzzle Games",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Unit",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Filters",
        "Topic :: Utilities"
    ]
)