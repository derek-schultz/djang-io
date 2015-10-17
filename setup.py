import sys
from setuptools import find_packages, setup

setup(
    name="djang-io",
    version="0.1",
    description="SocketIO integration for Django",
    author="Derek Schultz and D. P. Bulger",
    author_email='derek@quiet.af',
    platforms=["any"],
    license="MIT",
    url="http://github.com/derek-schultz/djang-io",
    packages=find_packages(),
    install_requires=[
        "Django",
        "eventlet==0.17.4",
        "greenlet==0.4.9",
        "python-engineio==0.7.0",
        "python-socketio==0.6.0",
        "six==1.10.0",
    ],
)
