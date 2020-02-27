# Release Notes

## 0.1.1
- [Issue 29](https://github.com/microsoft/topologic/issues/29) Fixed bug in `topologic.io.from_dataset` where an empty networkx graph object (Graph, DiGraph, etc) was being treated as if no networkx Graph object were provided at all.
- Added `is_digraph` parameter to `topologic.io.from_file`. This parameter defaults to False for original behavior. Setting it to True will create a networkx DiGraph object instead.

## 0.1.0
- Initial release

