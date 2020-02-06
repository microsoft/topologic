Creating and Analyzing an Embedding with `topologic`
===============

### Introduction to Embeddings
An embedding is a mapping from an object, such as a word, to a vector in a lower dimensional space. For 
example, an embedding for words into a 3 dimensional space could look something like:

```
cat -   [0.015269641674978685,   0.013187535371066428,  0.0031715410923515153]
dog -   [0.014965873253211082,   0.0016122454341539472, 0.0035909807224411283]   
man -   [0.004237593168056164,   0.003526102334225012,  0.0030491193727161248]
woman - [0.0031461043909993824,  0.010022862663402465,  0.040323956479097034]
king -  [0.00013326964708904043, 0.001007046442967896,  6.510123655167899e-05]
queen - [0.0013619392422438148,  0.006342057672591439,  0.002270385097256966]
```

Embeddings are useful because it allows for the calculation of similarity between two objects. By calculating the cosine
or Euclidian distance between two vectors in the embedding, you can determine the similarity between the two objects. 

### Create an Embedding
Creating an embedding from a graph using topologic is a straight-forward endeavor:
```
import topologic as tc
import networkx as nx

# create a graph
graph = nx.florentine_families_graph()

# create a graph embedding into a 300 dimensional space
embedding_dimensions = 300
embedding_container = tc.embedding.node2vec_embedding(
    graph,
    dimensions=embedding_dimensions
)

# extract the embedding and labels from the EmbeddingContainer
embedding = embedding_container.embedding
labels = embedding_container.vertex_labels

print(f'The shape of the entire embedding should be (number of nodes in graph x dimensions) which should be'
      f'({len(graph.nodes())}, {embedding_dimensions}) and is {embedding.shape}')
print(f'The length of first vector should be 300 and is {len(embedding[0])}')
print(f'The label for the first vector is {labels[0]}')
```

It should be noted that in most cases when you are wanting to generate a graph embedding you should be using only the 
largest connected component of the graph. To extract the largest connected component:
```
import topologic as tc
import networkx as nx

graph = nx.barbell_graph(50, 1)
largest_connected_component = tc.largest_connected_component(graph)
```

Several different embedding techniques are supported by the library. They can be found at topologic.embedding. It 
should be noted that for most embedding techniques, the graph needs to be weighted:

```
import topologic as tc
import networkx as nx

# create a graph
graph = nx.florentine_families_graph()

# apply default weight to the edges in the graph
for source, target in graph.edges():
            graph.add_edge(source, target, weight=1)
            
# create a graph embedding into a 300 dimensional space
embedding_dimensions = 300
embedding_container = tc.embedding.node2vec_embedding(
    graph,
    dimensions=embedding_dimensions
)
```

### Clustering
Essexgraphs offers a variety of clustering methods in the topologic.embedding.clustering module. Running a clustering
algorithm over an embedding will create a grouping of nodes that are similar. Following is an example of generating a 
clustering for an embedding using dbscan:


```
import networkx as nx
import topologic as tc

graph = nx.florentine_families_graph()
embedding_container = tc.embedding.node2vec_embedding(graph)

clustering = tc.embedding.clustering.dbscan(embedding_container.embedding)
                                                            
print(clustering)
```

The variable clustering will contain a list of labels that correspond to each vector in the embedding. For example,
```
clustering[0]
```
will be the label for the vector at 
```
embedding_container.embedding[0]
 ```
 which has the label
```
embedding_container.vertex_labels[0]
``` 
###### Clustering with Bayesian Information Criterion Optimizations 
Some clustering techniques supported in topologic require the specification of the number of clusters in the dataset.
Oftentimes it isn't obvious how many clusters are in a given dataset. One way of avoiding the specification of this
parameter is to calculate the clustering with different arguments for the number of clusters parameter and optimizing
the [Bayesian Information Criterion (BIC)](https://en.wikipedia.org/wiki/Bayesian_information_criterion). Essexgraphs
currently supports two ways of optimizing BIC for kmeans and gaussian mixture model clustering. The first is a linear
search:
```
import networkx as nx
import topologic as tc

graph = nx.florentine_families_graph()
embedding_container = tc.embedding.node2vec_embedding(graph)

clustering = tc.embedding.clustering.kmeans_with_bic_linear(
    embedding_container.embedding,
    min_clusters=2,
    max_clusters=15
)

print(f'Optimal number of clusters is {max(clustering) + 1')
``` 
Behind the scenes, kmeans will be calculated max_clusters - min_clusters times and the number of clusters selected will
optimize the BIC statistics. This is quite expensive and can take some time. Oftentimes, you can run this method once
for a embedding and then record the optimal number of clusters. Then you can revert back to normal kmeans method and
specify the number of clusters.  

###### Comparison of Clustering Techniques
For a comprehensive comparison of different clustering techniques see the 
[sklearn documentation](https://scikit-learn.org/stable/modules/clustering.html).
