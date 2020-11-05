# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import csv
import _csv  # typeshed is totally broken with csv module right now
import itertools
from io import StringIO
from typing import Iterator, List, Optional, TextIO, Union

from ..exceptions import DialectException


def _replace_invalid_characters(input_str: str) -> str:
    return input_str.replace("#", "")


class CsvDataset:

    # sys.maxsize works just fine on linux, but on windows it fails badly with the message
    # OverflowError: Python int too large to convert to C long
    # fun fact: any number > 2^31-1 makes it fail.  C long my butt.
    FIELD_SIZE_LIMIT = 2 ** 31 - 1

    def __init__(
        self,
        source_iterator: Union[TextIO, Iterator[str]],
        has_headers: Optional[bool] = None,
        dialect: Optional[Union[str, csv.Dialect]] = None,
        use_headers: Optional[List[str]] = None,
        sample_size: int = 50
    ):
        """
        Creates a CsvDataset based on the csv configuration information and the provided Iterator

        If configuration information is omitted for headers or dialect, we attempt to sniff it out based on a
        small sample size taken from the top of the iterator.

        :param Iterator[str] source_iterator: Any configured Iterator that will provide the underlying basis of our data
        :param Optional[bool] has_headers: True if we know it has headers, False if we know it does not, or None if we
            don't know
        :param dialect: If we know the dialect, we will use it.  If we don't know, it
            will be None and we'll attempt to sniff for it
        :type dialect: Optional[Union[str, csv.Dialect]]
        :param Optional[List[str]] use_headers: Provide known headers if we want to use them regardless of the
            underlying source.  If the underlying iterator still has headers present, ensure that has_headers is set to
            True.  *Note* use_headers takes precedence over any sniffing.
        :param int sample_size: Number of iterations through the iterator we should use to generate our sample set for
            sniffing.  Only used if we must sniff anything.  Defaults to 50 rows.
        :raises DialectException: If a dialect is not provided and one can not be reliably sniffed in the sample size
            provided
        """
        # remove all pound signs before use!  networkx Graphs behave very poorly if you have an octothorpe in them!
        filtered_source_iterator = map(_replace_invalid_characters, source_iterator)

        base_iterator, sniff_iterator = itertools.tee(filtered_source_iterator)

        sample_blob = self._sample_blob(dialect, has_headers, use_headers, sniff_iterator, sample_size)
        del sniff_iterator
        self._dialect: Union[_csv.Dialect, csv.Dialect] = csv.excel()

        if dialect is None:
            if sample_blob is None:
                raise DialectException(
                    "A dialect was not provided and one was not able to be sniffed; a sample was unable to be obtained"
                    " from the csv reader"
                )
            sniffed_dialect = csv.Sniffer().sniff(sample_blob)
            if sniffed_dialect is None:
                raise DialectException(
                    f"A dialect was not provided and one was not able to be sniffed with a sample size of {sample_size}"
                )
            self._dialect = sniffed_dialect()
        else:
            if isinstance(dialect, csv.Dialect) or isinstance(dialect, _csv.Dialect):
                self._dialect = dialect
            else:
                self._dialect = csv.get_dialect(dialect)

        csv.field_size_limit(self.FIELD_SIZE_LIMIT)
        self._csv_reader: Iterator[List[str]] = csv.reader(base_iterator, self._dialect)

        if use_headers is not None:
            # regardless, use the configured values
            self._headers = use_headers
            if has_headers:
                # advance the reader
                next(self._csv_reader)
        elif has_headers is True:
            # we weren't given headers to use and we were told there are headers, so we're using those
            self._headers = next(self._csv_reader)
        else:
            if sample_blob is None:
                raise Exception(f"Unable to read any data from {source_iterator} to read headers")
            if has_headers is False or not csv.Sniffer().has_header(sample_blob):
                # generating our own based on a the the maximum count of columns in our sample set
                self._headers = self._generate_headers(sample_blob)
            else:
                # has headers is None and the sniffer thinks it found something
                self._headers = next(self._csv_reader)

    def _generate_headers(self, sample_blob: str) -> List[str]:
        sample_reader = csv.reader(StringIO(sample_blob), self._dialect)
        max_column_count = max(map(lambda x: len(x), sample_reader))
        return list(map(lambda x: f"Attribute {x}", range(0, max_column_count)))

    def _should_collect_sample(self, dialect: str, has_headers: Optional[bool], use_headers: List[str]) -> bool:
        # if a dialect isn't provided, we collect a sample to use in sniffing
        # if we aren't told about header existence or we are told there are no headers and we are not given a set of
        # headers to use instead, we will collect a sample to use in header generation
        if dialect is None:
            return True
        if use_headers is None and has_headers is not True:
            return True
        return False

    def _sample_blob(
        self,
        dialect,
        has_headers,
        use_headers,
        sniff_iterator,
        sample_size
    ) -> Optional[str]:
        if self._should_collect_sample(dialect, has_headers, use_headers):
            return "".join(
                self._extract_sample(
                    sniff_iterator,
                    sample_size
                )
            )
        return None

    @staticmethod
    def _extract_sample(sniff_iterator: Iterator[str], sample_size: int) -> List[str]:
        sample = list(itertools.islice(sniff_iterator, sample_size))
        return sample

    def headers(self) -> List[str]:
        """
        :return: Returns a *copy* of the headers.
        :rtype: List[str]
        """
        return self._headers.copy()

    def reader(self) -> Iterator[List[str]]:
        """
        :return: Returns a properly configured csv reader for a given dialect
        :rtype: Iterator[List[str]]
        """
        return self._csv_reader

    def dialect(self) -> Union[_csv.Dialect, csv.Dialect]:
        """
        Note: return type information is broken due to typeshed issues with the csv module.

        :return: Dialect used within this CsvDataset for the csv.reader.
        :rtype: Union[_csv.Dialect, csv.Dialect]
        """
        return self._dialect
