# Topologic

## Topologic is now Deprecated
Please use [Graspologic](https://github.com/microsoft/graspologic) instead.

[![Documentation Status](https://readthedocs.org/projects/topologic/badge/?version=latest)](https://topologic.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/topologic)](https://pypi.org/project/topologic/)

## Release Status
Version 0.1.1 is released! 
- [PyPI](https://pypi.org/project/topologic/)
- [ReadTheDocs](https://topologic.readthedocs.io/)

## Installation Instructions
```python
pip install topologic
```

## Plans
- None - see deprecation message above

## Bugs or Feature Requests
Please file a new [issue](https://github.com/microsoft/topologic/issues/new) if you find any bugs, either in the code or the documentation.

## Development Setup Instructions
Topologic was developed for Python 3.6+ and makes extensive use of type hints throughout and _f_-strings throughout. Python 2.7 is not supported.

Topologic is known to work with Python x64 3.6, 3.7, and 3.8 on Windows and Ubuntu, and presumed to work on MacOS as well. Please submit a new [issue](https://github.com/microsoft/topologic/issues/new) with any issues found on any of these versions.

### Windows
```cmd
py -m venv venv
venv\Scripts\activate.bat
pip install -U setuptools wheel pip
pip install -r requirements.txt
```
It is possible that you will need to install Visual Studio Build Tools for some of the `topologic` dependencies. Some dependencies such as scipy and numpy have C code that must be compiled for your version of Python to work. Please follow the directions in your console if you have errors after installing the requirements and then try again after following these instructions.

### MacOS
```bash
python3 -m venv venv
source venv/bin/activate
pip install -U setuptools wheel pip
pip install -r requirements.txt
```

### Ubuntu
```bash
sudo apt-get update && sudo apt-get install python3-pip python3-dev
python3 -m venv venv
source venv/bin/activate
pip install -U setuptools wheel pip
pip install -r requirements.txt
```

### Running Tests

```bash
mypy ./topologic
mypy ./tests
flake8 ./topologic ./tests
pytest tests topologic
```

# Contributing

This project welcomes contributions and suggestions. Most contributions require you to
agree to a Contributor License Agreement (CLA) declaring that you have the right to,
and actually do, grant us the rights to use your contribution. For details, visit
https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need
to provide a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the
instructions provided by the bot. You will only need to do this once across all repositories using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)
or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

# Privacy

`topologic` does not collect, store, or transmit any information of any kind back to Microsoft.

For your convenience, here is the link to the general [Microsoft Privacy Statement](https://privacy.microsoft.com/en-us/privacystatement/). 
