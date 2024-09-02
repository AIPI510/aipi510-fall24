from setuptools import setup, find_packages

setup(
    name='pokeapi_assignment',
    version='0.1',
    py_modules=['main'],
    install_requires=[],
    entry_points='''
        [console_scripts]
        pokeapi=pokeapi:main
    ''',
)