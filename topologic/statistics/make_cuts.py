# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
from enum import Enum
from typing import Any, Callable, Tuple, Union


class MakeCuts(Enum):
    LARGER_THAN_INCLUSIVE = 1
    LARGER_THAN_EXCLUSIVE = 2
    SMALLER_THAN_INCLUSIVE = 3
    SMALLER_THAN_EXCLUSIVE = 4


# for internal use
def filter_function_for_make_cuts(
    cut_threshold: Union[int, float],
    cut_process: MakeCuts
) -> Callable[[Tuple[Any, Union[int, float]]], bool]:
    filter_function = {
        MakeCuts.LARGER_THAN_EXCLUSIVE: lambda x: x[1] > cut_threshold,
        MakeCuts.LARGER_THAN_INCLUSIVE: lambda x: x[1] >= cut_threshold,
        MakeCuts.SMALLER_THAN_EXCLUSIVE: lambda x: x[1] < cut_threshold,
        MakeCuts.SMALLER_THAN_INCLUSIVE: lambda x: x[1] <= cut_threshold
    }
    if cut_process not in filter_function:
        raise ValueError("Provided cut_process is not a valid MakeCuts enum value.")
    return filter_function[cut_process]
