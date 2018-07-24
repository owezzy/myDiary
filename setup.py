from setuptools import setup, find_packages

setup(
    name='diary-api',
    packages=find_packages(where='api'),
    package_dir={'': 'api'},
)
