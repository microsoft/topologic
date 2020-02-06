# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from ..metadata_types import MetadataTypeRegistry
from typing import Dict, List, Optional

ATTRIBUTES = "attributes"


def metadata_to_dict(
    values: List[str],
    ignore_columns: List[int],
    ignored_values: Optional[List[str]],
    keys: List[str],
    types_registry: MetadataTypeRegistry
) -> Dict[str, str]:
    """
    Converts two parallel lists of values into a dictionary of key value pairs.

    This function is ultimately a more complex dict(zip(keys,values)) function.

    Ideally, len(values) == len(keys).  Only iterates through min(len(values), len(keys)) to avoid any overruns.

    Mismatched sizes could mean invalid data, but due to the relatively lax rules of CSV, could also be valid data.

    Will use ignore_columns to skip over columns in both lists that correspond with that integer.  No key or value will
    be written for these columns.

    Will also use any value provided in ignore_values to ignore adding any value that matches.  This allows us to avoid
    adding usually skipped data such as NULL or N/A or "" as metadata attributes.

    As each valid key:value pair is identified, they will be registered with the passed in MetadataTypeRegistry where
    each value is tested for type.  A record of the most-universally-successful narrow precision type will be captured

    :param List[str] values: The data values will be the values of the resulting dictionary.  List can be empty, but
        cannot be None.
    :param List[int] ignore_columns: A list of column indices to be skipped over.  List can be empty, but cannot be None
    :param List[str] ignored_values: A list of invalid values to avoid if they exist in the row list.  List can be
        empty, but cannot be None.
    :param List[str] keys: A list of the keys to be used as the key in the resulting dictionary.  These are most often
        from the headers of a CsvFile or the attribute name in a JSON file.  List can be empty, but cannot be None.
    :param MetadataTypeRegistry types_registry: If all values for a given key are numeric, this captures that for later
        usage in any schema specification.  If any value for a given key are of less precision, all values are treated
        as that wider type.
    :return: An attribute dictionary
    :rtype: dict[str, str]
    """
    actual_ignored_values = [] if ignored_values is None else ignored_values
    min_length = min(len(values), len(keys))
    metadata = {}
    for i in range(0, min_length):
        header = keys[i]
        value = values[i]
        if i not in ignore_columns and value not in actual_ignored_values:
            types_registry.register(header, value)
            metadata[header] = value
    return metadata
