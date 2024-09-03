from setuptools import setup, find_packages

setup(
    name = "SourceSavvy"
    version= "0.1.0"
    description="This project showcases a user's recent activities using the strava API"
    author="Jinyoung Suh", "Harshitha Rasamsetty"
    author_email= "violaseo1024@gmail.com", "harshir07@gmail.com"
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "geopandas"
        "requests",
    ],
    tests_requires=[
        "unittest"
    ],
    entry_points={
        "console_scripts":[
            "SourceSavvy=api_strava:main",
        ]    
    },
    python_requires=">=3.6",
)