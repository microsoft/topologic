# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.


class UnweightedGraphError(BaseException):
    def __init__(self, message):
        self.message = message


class InvalidGraphError(BaseException):
    def __init__(self, message):
        self.message = message


class DialectException(BaseException):
    def __init__(self, message):
        self.message = message
