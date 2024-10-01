from setuptools import setup, find_packages

setup(
    name='coin_flip_p_value_analysis',
    version='0.1',
    description='A project to analyze p-values from coin flip simulations using various statistical tests.',
    author='Vishnu & Bryant',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'scipy>=1.7.0',
        'seaborn>=0.11.0',
        'matplotlib>=3.4.0',
        'pytest>=6.0.0',
        'setup.py>=75.1.0'
    ],
    entry_points={
        'console_scripts': [
            'coin_flip=p_values:main',  
        ],
    },
)
