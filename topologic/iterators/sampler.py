# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.


class Sampler:

    @staticmethod
    def sample(iterable, sample_size):
        index = 0
        returned_items = 0

        for current in iterable:

            # The first quarter of the sample should be the top rows of the file (including the header if
            # one is present).  The next quarter of the sample is every tenth row starting at the end of the first
            # sample.  The last half of the sample is every 30th row.  This will spread the samples out throughout the
            # file unless the file is very large while ensuring that a chunk of the samples are continuous.  Continuous
            # rows are helpful when neighboring rows share graph nodes.
            if returned_items < (sample_size / 4) \
                    or (returned_items < sample_size / 2 and index % 10 == 0) \
                    or index % 30 == 0:
                returned_items += 1
                yield current

            index += 1

            if returned_items == sample_size:
                break
