"""
topologic.projections provides a canned series of source-to-Graph projection functions.

The function return type Callable[[nx.Graph], Callable[[List[str]], None]] is the cornerstone
to every projection function.

You can, and should, define any function you want as long as it complies with that return type.  The first function
should take in any Dataset source-specific configuration information; information necessary to tell a projection
function how your source data is laid out and should be used to apply changes to the networkx.Graph.

The 1st inner function is used by the topologic.io.csv_loader.from_dataset function - it applies the networkx.Graph
to update.

The 2nd inner function is also used by topologic.io.csv_loader.from_dataset to take each record from the Dataset
source and use it to apply this modification to the networkx.Graph.

Graph metadata format:

If a graph is to have metadata on its vertices or edges, it shall always be in the form of:

.. code-block:: json

    {
        "weight": 1.0,
        "attributes": [
            { "key": "value1", "anotherKey": "anotherValue", "aDifferentKey": "aDifferentValue" },
            { "key": "value2", "aDifferentKey": "aDifferentValue2" }
        ]
    }

Notes:
- Keys are always of type str
- Values are always stored as type str, but could be a more narrowly bounded type like int or float.
- Just because a key exists in one row of the attributes List does not mean it will exist in any other.  Do not
presume a constant "shape" of the dictionaries of edge attributes.

"""
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from .edge_projections import edge_with_collection_metadata, edge_with_single_metadata, edge_ignore_metadata
from .vertex_projections import vertex_with_collection_metadata, vertex_with_single_metadata

__all__ = [
    "edge_ignore_metadata",
    "edge_with_collection_metadata",
    "edge_with_single_metadata",
    "vertex_with_collection_metadata",
    "vertex_with_single_metadata"
]
