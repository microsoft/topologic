# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.


class PotentialEdgeColumnPair:
    def __init__(self, source, destination, score):
        self._source = source
        self._destination = destination
        self._score = score

    def source(self):
        return self._source

    def destination(self):
        return self._destination

    def score(self):
        return self._score
