import os
from setuptools import find_packages
from setuptools import setup

setup(
    name='motion_action',
    version='0.0.0',
    packages=find_packages(
        include=('motion_action', 'motion_action.*')),
)
