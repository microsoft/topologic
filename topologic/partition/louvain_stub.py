# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import community


_fixed_best_partition_docstring = community.best_partition.__doc__.replace(
    "community.best_partition",
    "topologic.partition.louvain"
).replace(
    "community(",
    "louvain("
).replace(
    ".. 1.",
    "1."
).replace(
    "Uses Louvain algorithm",
    "This louvain function is an alias to the " \
    "`community.best_partition <https://python-louvain.readthedocs.io/en/latest/api.html#community.best_partition>`_ function" \
    " in the `python-louvain <https://github.com/taynaud/python-louvain>`_ library written by " \
    "`Thomas Aynaud <https://github.com/taynaud>`_. "
)

# Documentation note: see docs/topologic.partition.rst for document string to louvain function alias
louvain = community.best_partition
louvain.__doc__ = _fixed_best_partition_docstring
