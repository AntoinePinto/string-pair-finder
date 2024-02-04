from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='stringpairfinder',
    version='1.0.0',
    description='Package designed to match strings by similarity',
    author='Antoine PINTO',
    author_email='antoine.pinto1@outlook.fr',
    license='MIT',
    license_file='LICENSE',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/AntoinePinto/string-pair-finder',
    project_urls={
        'Source Code': 'https://github.com/AntoinePinto/easyenvi',
    },
    keywords=["string", "string matching", "algorithm", "similarity"],
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.6"
    ],
    python_requires='>=3.7'
)