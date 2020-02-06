# Topologic

## Release Status
Topologic has yet to be published to [PyPi](https://pypi.org/), and the documentation has yet to be generated and published to [Read the Docs](https://readthedocs.org/).

## Bugs or Feature Requests
Please file a new [issue](https://github.com/microsoft/topologic/issues/new) if you find any bugs, either in the code or the documentation.

## Development Setup Instructions
Topologic was developed for Python 3.5+ and makes extensive use of type hints throughout. Python 2.7 is not supported.

Topologic is known to work with Python x64 3.6, 3.7, and 3.8 on Windows and Ubuntu, and presumed to work on MacOS as well. Please submit a new [issue](https://github.com/microsoft/topologic/issues/new) with any issues

### Windows
TODO: instructions

### MacOS
TODO: instructions

### Ubuntu
```bash
sudo apt-get update && sudo apt-get install python3-pip python3-dev
sudo python -m venv venv
source venv/bin/activate
pip install -U setuptools wheel
```

### Running Tests

```bash
mypy -m topologic
mypy -m tests
flake8 ./topologic ./tests
pytest tests topologic --doctest-modules
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
