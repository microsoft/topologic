# Release Notes
## 0.1.3
- Fix bug when getting the length of edges when performing graph augmentations.
## 0.1.2
- Rename `self_loop_augmentation` to `diagonal_augmentation` and use weighted degree to perform calculation instead of degree only.
## 0.1.1
- [Issue 29](https://github.com/microsoft/topologic/issues/29) Fixed bug in `topologic.io.from_dataset` where an empty networkx graph object (Graph, DiGraph, etc) was being treated as if no networkx Graph object were provided at all.
- Added `is_digraph` parameter to `topologic.io.from_file`. This parameter defaults to False for original behavior. Setting it to True will create a networkx DiGraph object instead.

## 0.1.0
- Initial release

