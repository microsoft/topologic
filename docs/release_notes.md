# Release Notes
## 0.1.8
- Fix an issue with sorting non integer node ids when calculating omnibus embeddings
## 0.1.7
- Use the union graph largest connected component strategy to calculate the omnibus embedding
## 0.1.6
- Fix an issue that caused inf and nan when using LSE omnibus embedding
## 0.1.5
- Fix a bug in omnibus embedding where augmentation happened before the graphs were reduced to common nodes
## 0.1.4
- Fixed a bug during Laplacian matrix construction for directed graphs
## 0.1.3
- Added `modularity` and `modularity_components` functions, and deprecated `q_score`.
## 0.1.2
- Rename `self_loop_augmentation` to `diagonal_augmentation` and use weighted degree to perform calculation instead of degree only.
- Fix bug when getting the length of edges when performing graph augmentations.
## 0.1.1
- [Issue 29](https://github.com/microsoft/topologic/issues/29) Fixed bug in `topologic.io.from_dataset` where an empty networkx graph object (Graph, DiGraph, etc) was being treated as if no networkx Graph object were provided at all.
- Added `is_digraph` parameter to `topologic.io.from_file`. This parameter defaults to False for original behavior. Setting it to True will create a networkx DiGraph object instead.

## 0.1.0
- Initial release

