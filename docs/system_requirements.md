# System Requirements

`topologic` is written for Python 3.6.  It is well tested under Python 3.7 and may work well with Python 3.8.  It makes use of type hinting heavily, so it is not likely to work with Python 3.5.

In addition, some of the library dependencies for `topologic` must be built on your system, and will require C++ build tools to complete.  If you don't already have these, the install process will fail, and you can try some of the following steps to fix your issues.

## Windows
Visit [Visual Studio](https://visualstudio.microsoft.com/downloads/) and select the `Tools for Visual Studio 2017` header.  Then download and install the `Build Tools for Visual Studio 2017`.

## Ubuntu Linux
If using Python3.6:

```bash
sudo apt install build-essential python3.6-dev
```

If using Python3.7:

```bash
sudo apt install build-essential python3.7-dev
```

