from distutils.core import setup
from setuptools import find_packages

setup(
    name="word-squeezer",
    version="1.0.0",
    description="Word finding games",
    author="pablohonney",
    packages=find_packages(exclude=["tests"]),
    extras_require={"tests": ["pytest"]},
    entry_points={
        "console_scripts": [
            "word-squeezer = word_squeezer.word_squeezer:main",
            "wordament = word_squeezer.wordament_solver:main",
        ],
    },
)
