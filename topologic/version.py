# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import datetime
from typing import List, Optional, Tuple
import pkg_resources
from . import __name__ as package_name

__all__: List[str] = ["get_version_and_type", "get_version"]

# manually updated
__semver = "0.1.0"

__version_file = "version.txt"


def _from_resource() -> str:
    version_file = pkg_resources.resource_stream(package_name, __version_file)
    version_file_contents = version_file.read()
    return version_file_contents.decode("utf-8").strip()


def _from_path(path: str) -> str:
    with open(path) as version_file:
        version_line = version_file.readline()
        return version_line.strip()


def version_file_as_str(version_file_path: Optional[str]) -> str:
    # in most cases, we want to treat this as a package relative file
    if version_file_path is None:
        return _from_resource()
    else:
        # however, if we need to get the version prior to calling setuptools, we need to read from a file instead
        return _from_path(version_file_path)


def local_build_number() -> str:
    return datetime.datetime.today().strftime('%Y%m%d.0+local')


def version_from_file(version_file_path: Optional[str] = None) -> Tuple[str, str]:
    build_type: str = ""
    build_number: str = ""
    try:
        version_file_contents: str = version_file_as_str(version_file_path)
        if len(version_file_contents) == 0:
            raise ValueError("Empty file, fallback to local snapshot")
        version_file_values = version_file_contents.strip().split(",")
        if len(version_file_values) == 2:
            temp_type = version_file_values[0].lower()
            temp_build_number = version_file_values[1]
            timestamp, daily_build_number = temp_build_number.split(".")
            combined_build_number = f"{timestamp}{daily_build_number.rjust(3, '0')}"

            if temp_type == "snapshot" or temp_type == "release":
                build_type = temp_type
                build_number = combined_build_number
            else:
                raise ValueError("Unknown build type, fallback to local snapshot")
        else:
            raise ValueError("Unknown version file format, fallback to local snapshot")
    except (FileNotFoundError, ValueError):
        build_type = "snapshot"
        build_number = local_build_number()
    return build_type, build_number


def get_version_and_type(version_file_path: Optional[str] = None) -> Tuple[str, str]:
    build_type, build_number = version_from_file(version_file_path)
    return (f"{__semver}.dev{build_number}", build_type) if build_type == "snapshot" else (__semver, build_type)


def get_version(version_file_path: Optional[str] = None) -> str:
    version, _ = get_version_and_type(version_file_path)
    return version
