# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from typing import Dict


class MetadataTypeRegistry:

    _type_chain: Dict[type, type] = {int: float, float: str, str: type(None)}

    def __init__(self):
        self._attributes_and_likely_types: Dict[str, type] = {}

    def attribute_to_type_mapping(self) -> Dict[str, type]:
        """
        Returns a *copy* of the attributes and likely types dictionary.
        This dictionary should be safe to use for typing each attribute.  However, it may also be less restrictive
        than the user would like - but since we are inferring the types this is the best we should hope for.

        :return: Returns a *copy* of the attributes and likely types dictionary.
        :rtype: dict[str, type]
        """
        return self._attributes_and_likely_types.copy()

    def register(
        self,
        attribute: str,
        value: str
    ) -> type:
        """
        Endeavours to attempt to coerce the type from most restrictive to least restrictive.

        If a given attribute is already marked as being a string, no coercion is attempted.
        If a given attribute is already marked as being an int, only int coercion is attempted.
        If a given attribute is already marked as being a float, float will be attempted, upon failure int, and
        upon failure string

        :param str attribute: The attribute name that will be associated with the discerned type
        :param str value: The value that we will attempt to coerce
        """
        # mypy was not keen on dict.get(foo, <type>)
        type_attempt = int if attribute not in self._attributes_and_likely_types \
            else self._attributes_and_likely_types[attribute]
        actual_type = self._recursive_type_chain(type_attempt, value)
        self._attributes_and_likely_types[attribute] = actual_type
        return actual_type

    def _recursive_type_chain(
            self,
            type_attempt: type,
            value: str
    ) -> type:
        try:
            type_attempt(value)
            return type_attempt
        except ValueError:
            if self._type_chain[type_attempt]:
                return self._recursive_type_chain(self._type_chain[type_attempt], value)
            else:
                return type_attempt
