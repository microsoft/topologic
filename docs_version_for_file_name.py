# Copyright (C) Microsoft Corporation. All rights reserved.

from topologic import version

version, build_type = version.get_version_and_type()

if build_type == "release":
    print(f"{version}-RELEASE")
else:
    print(version)

