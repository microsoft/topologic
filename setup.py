# Copyright (C) Microsoft Corporation. All rights reserved.
import setuptools
import sys
import os


def handle_version() -> str:
    sys.path.insert(0, os.path.join("topologic", "version"))
    from version import version
    sys.path.pop(0)

    version_path = os.path.join("topologic", "version", "version.txt")
    with open(version_path, "w") as version_file:
        b = version_file.write(f"{version}")
    return version


version = handle_version()

setuptools.setup(
    name="topologic",
    description="Topologic is a network/graph library for the creation of embeddings from networkx graphs using "
                "adjacency spectral embedding, laplacian spectral embedding, node2vec embeddings, and omnibus "
                "embeddings. It also includes a lot of utilities and quality of life functions for loading and "
                "processing networkx graph objects and statistical analysis over these objects.",
    version=version,
    packages=setuptools.find_packages(exclude=["tests", "tests.*", "tests/*"]),
    package_data={'version': [os.path.join('topologic', 'version', 'version.txt')]},
    include_package_data=True,
    author="Dwayne Pryce",
    author_email="dwpryce@microsoft.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    project_urls = {
        "Github": "https://github.com/microsoft/topologic",
        "Documentation": "https://topologic.readthedocs.io",
    },
    url="https://github.com/microsoft/topologic",
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
            'sphinx>=2.4.4,<3.0.0',
            'sphinx-rtd-theme',
            'testfixtures',
            'recommonmark'
        ],
    }
)
