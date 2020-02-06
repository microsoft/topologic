# Copyright (C) Microsoft Corporation. All rights reserved.
import setuptools
import os

# Python 3 + build tools are required to install this library. To install the
# prerequisites on Ubuntu, run
# sudo apt-get install build-essential python3 python3-dev python3-venv

version_file_path = os.path.abspath("topologic/version.txt")
exec(open('topologic/version.py').read())

version = get_version(version_file_path)

setuptools.setup(
    name="topologic",
    description="Topologic is a network/graph library for the creation of embeddings from networkx graphs using "
                "adjacency spectral embedding, laplacian spectral embedding, node2vec embeddings, and omnibus "
                "embeddings. It also includes a lot of utilities and quality of life functions for loading and "
                "processing networkx graph objects and statistical analysis over these objects.",
    version=version,
    packages=setuptools.find_packages(exclude=["tests", "tests.*", "tests/*"]),
    package_data={'': ['version.txt']},
    include_package_data=True,
    author="Dwayne Pryce",
    author_email="dwpryce@microsoft.com",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires=[
        'networkx',
        'python-louvain>=0.13',
        'numpy',
        'scipy',
        'sklearn',
        'gensim'
    ],
    extras_require={
        'devtools': [
            'pytest',
            'flake8',
            'mypy',
            'sphinx',
            'sphinx-rtd-theme',
            'testfixtures',
            'recommonmark'
        ],
    }
)
