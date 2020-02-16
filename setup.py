#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("requirements.txt","r") as dependencies:
    requirements = dependencies.readlines()

print(find_packages())
setup(
    name='MrRobot',
    version='1.0.0',
    description='Just another robot to automate the hacking process',
    author='Kike Fontan (@CosasDePuma)',
    author_email='kikefontanlorenzo@gmail.com',
    url='https://www.github.com/cosasdepuma/mrrobot',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={ 'console_scripts': ['mrrobot=mrrobot:entrypoint'] }
)