# encoding: utf:8 
"""
@author: Joey
@contact: zengjiayi666@gmail.com
@file: setup.py.py
@time: 2022/4/17 22:06
"""

from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
