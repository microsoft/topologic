# ETL for Graphs in `topologic`

## Summary

Pulling graph data out of source files is an ubiquitous task for any data scientist.  `topologic` provides some 
capabilities to assist some of the more common processes in the `topologic.io` and `topologic.projection` packages.

These functions can seem quite complex initially, but they're designed that way to make sure a wide and disparate 
number of different use cases can be accomodated.

This tutorial aims to start with the simplest cases and move on to more and more complex ones, showing how you can
make your own csv-row-based processing functions to achieve useful behaviors well outside the general purpose functions
built in to the library.

**Note**: Most examples presume your graph is undirected.

## Examples
The first example, using `from_file` will try to absolve you, the user, of knowing much of how your csv file turns into 
a graph.  However, your specific use case is very likely outside the few prepackaged scenarios we've anticipated.

In the second example, we'll show you how `from_file` is just a simple helper over the much more powerful (but lower 
level) `from_dataset` function.  We'll do the exact same task, using the same library provided functions, but tailored
very closely to our specific data.

In the third example, we'll take the second and modify it to show you how you can provide your own custom logic for 
merging multiple connections between the same vertices into a single edge.

And in the last example, we will presume we have a very massive data file, and wish to exclude certain edge connections
based on an edge threshold mechanic.

## Edges and Weights Only

Let's start with a tsv file; a row and column format with the columns separated by the tab character `\t` and a 
newline character `\n`.  (Note that it could also be `\r\n` - the library should be able to handle this without trouble)

`my_edges.tsv`
```
time	date	quantity	distributor	vendor
08:01	2019-01-02	58	widgets, inc.	big box enterprises
08:03	2019-01-02	103	widgets, inc.	blue big box corp
08:03	2019-01-02	1000	widgets, inc.	fabricatrix
08:04	2019-01-02	5	ferrous machine company	widgets, inc.
08:04	2019-01-02	300	ferrous machine company	automotive R&D X
08:05	2019-01-02	10	parent automotive company	automotive R&D X
08:07	2019-01-02	10	parent automotive company	Your Local Auto Dealer
08:07	2019-01-03	2	parent automotive company	Your Local Auto Dealer
```   

This is a terribly tiny completely fabricated graph used primarily to illustrate loading the edges of the graph.

Let's presume this file exists at the file path `/path/to/my_edges.tsv`.  
#### The Easiest Way To Load This Graph (`load`)
```python
import networkx as nx
from topologic.io import load

graph: nx.Graph = load(
    edge_file="/path/to/my_edges.tsv",
    separator="excel-tab",
    has_header=True,
    source_index=3,
    target_index=4,
    weight_index=2
)


```
This will read a file at path at `edge_file` that is a csv with a header where the first column is the source node id,
the second columns is the target node id, and the third column contains the weights for each edge.

#### The Easy Way To Load This Graph (`from_file`)
```python
import networkx as nx
from topologic.io import from_file, GraphContainer

with open("/path/to/my_edges.tsv", "r") as edge_file:
    graph_container: GraphContainer = from_file(
        edge_csv_file=edge_file,
        source_column_index=3,  # note that we start counting from 0.
        target_column_index=4,
        weight_column_index=2,
        edge_csv_has_headers=True,
        edge_dialect="excel-tab",
        edge_metadata_behavior="none"
    )
    
graph: nx.Graph = graph_container.graph

```  

Let's take a second to unpack what we just did.

The `topologic.io.from_file` function takes in an open file, a `TextIO`.  It does not take in a string path - you 
have to open the file yourself.

It also asks for the indexes of the 3 important columns: source, target, and weight.  If you check the API docs, you'll
find that the `weight_column_index` is actually optional.  If you have no specific weight for an edge, it calculates one
for you based on the number of times it has seen a connection between `A` and `B`.  

It allows us to specify whether the edge csv file has headers - though this is also an optional parameter.  If you say
nothing, we try to do our best to determine whether there are actually headers or not - using the `csv` module's Sniffer
class.

It also allows us to specify whether the edge csf file has a specific dialect; once again, this is an optional 
parameter.  If you say nothing, we once again try to do our best to determine the most likely dialect based on a small
sample of your data (about 50 lines or so).  Once again, this is using the `csv` module's Sniffer class.

The last parameter can actually be left off, but it's important to know what options you have; the 
`edge_metadata_behavior` tells the underlying parser what it should do with each row from the csv.  The built-in 
capabilities are:
- `none`: Ignore everything about the edge except the `source`, `target`, and `weight` (if it exists).  Every other column
is dropped and will not be present in the final `networkx.Graph` object.
- `simple`: Every column that is not the `source`, `target`, and `weight` columns are added to the graph's edge metadata
The main problem is that if your edge list contains multiple entries about the undirected relationship between `A` and
`B`, for every column other than the `weight`, it adds it as an edge metadata attribute.  *This presents a last-in-wins
scenario* for your graph.  There are even more ramifications we will go into more in depth later.  Suffice to say that 
`simple` doesn't mean a simple process - it means your data is simple and we shouldn't worry about many special rules.
- `collection`: This behavior is actually probably simpler than the `simple` behavior.  It is intended to turn an
undirected Multigraph into an undirected Graph, by merging the edges.  The weights are aggregated, the metadata for each
row is stored as a List of Dictionary attributes, and no data is lost.  It is another simplistic model for handling 
data that has not been appropriately pre-processed.

**Vital Note**: All 3 of these provided functions do the same thing if an edge from `A` to `B` currently exists; they 
sum the weights.  Regardless of how their metadata is dealt with, the weights *are combined (including signs, e.g. 
weight -10 and weight 11 result in a weight of 1)

As you can see even now, these 3 processes have a number of limitations, some unique, some not.  If none of these will 
meet your needs, read on!

#### Harder Way to Load This Graph (`from_dataset`)

The previous example tried to absolve you, the user, of knowing much of how your csv file turns into a graph.  However,
your specific use case is very likely outside the realm of those 3 `edge_metadata_behavior` options, and the truth is
`from_file` is just a helper function for the far more powerful `from_dataset` function.

The point of `from_dataset` is to allow you to specify a number of different `topologic.io.CsvDataset` objects with
their own configuration data, select a number of different *csv row projection functions*, and call `from_dataset`
over the same `networkx.Graph` object, but with different combinations of `CsvDataset` and 
*csv row projection functions* to achieve your needs.

The following code is just an example scenario.  In it, we will show how you can accomplish the same task as above, but 
can have fine control over every behavior the ETL process requires.

```python
from topologic.io import CsvDataset, from_dataset
from topologic.projection import edge_ignore_metadata

with open("/path/to/my_edges.tsv", "r") as edge_file:
    csv_dataset = CsvDataset(
        source_iterator=edge_file,
        has_headers=True,
        dialect="excel-tab"
    )
    
    edge_projection_function = edge_ignore_metadata(
        source_index=3, 
        target_index=4, 
        weight_index=2
    )
    
    graph, _ = from_dataset(
        csv_dataset=csv_dataset,
        projection_function_generator=edge_projection_function
    )
```

The original way is 14 lines of code, the modified way is 21 - there's a reason the first exists, after all.  But now 
let's imagine another scenario.

#### Different Way to Load This Graph
If you noticed in the sample data above, there are two entries for the same connection between `parent automotive 
company` and `Your Local Auto Dealer`.  What if we don't want to sum these weights - what if we wanted to average them?

The following code will show you how to accomodate that behavior.

```python
import networkx as nx
from topologic import MetadataTypeRegistry 
from topologic.io import CsvDataset, from_dataset
from typing import Any, Callable, Dict, List


# set up the following projection generator.  See the API documentation in topologic.projection for details on
# the contract you must adhere to
def _averaging_edge_projection_generator(
    source_index_column: int,
    target_index_column: int,
    weight_index_column: int
) -> Callable[[nx.Graph, MetadataTypeRegistry], Callable[[List[str]], None]]:

    def _configure_graph_and_type_registry(
        graph: nx.Graph,
        type_registry: MetadataTypeRegistry  # the from_dataset contract will require this, but we don't need to use it
    ) -> Callable[[List[str]], None]:
        def _average_edge(row: List[str]):
            # since we already know everything there is to know about this data format, we don't need to
            # protect ourselves with length checks or anything like that.  our data is flawless!
            # but if it wasn't flawless, here is where you should handle it, by either adding nothing to the graph,
            # or adding what you feel you safely can
            source = row[source_index_column]
            target = row[target_index_column]
            weight = float(row[weight_index_column])
            
            if source in graph and target in graph and target in graph[source]:
                # this connection already exists!
                attributes = graph[source][target]
                attributes["_sum"] += weight
                attributes["_count"] += 1
                attributes["weight"] = attributes["_sum"] / attributes["_count"]                
            else:
                attributes: Dict[Any, Any] = {
                    "_count": 1,
                    "_sum": weight
                    "weight": weight
                }
                graph.add_edge(source, target, **attributes)
        return _average_edge
    return _configure_graph_and_type_registry

with open("/path/to/my_edges.tsv", "r") as edge_file:
    csv_dataset = CsvDataset(
        source_iterator=edge_file,
        has_headers=True,
        dialect="excel-tab"
    )
    
    graph, _ = from_dataset(
        csv_dataset,
        _averaging_edge_projection_generator(3, 4, 2)
    )

```

The 3-tier partially applied function is possibly daunting, but most of it is just so we can provide the right 
configuration information at the start, the right graph and type registry when we need to, and then process a 
row of strings and modify the graph accordingly!  

#### Large Graph We Need to Shrink
Some datasets contain too much data to store at one time.  The following tutorial will show you how to go about 
harnessing the power of `itertools.tee()` to pre-process the source file and gather the information we need to define
a edge cut threshold; values below a certain threshold can be ignored and we never need to elevate these entries into
the actual networkx graph.  Further, we absolutely want to totally clobber any existing entries between `A` and `B`, 
including their weights.

Presume we have the same file format as before, but it's 20gb or so in size.

```python
import networkx as nx
import numpy as np
from topologic import MetadataTypeRegistry 
from topologic.io import CsvDataset, from_dataset
from itertools import tee
from typing import Callable, List
import csv


# set up the following projection generator.  See the API documentation in topologic.projection for details on
# the contract you must adhere to
def _only_edges_above(
    source_index_column: int,
    target_index_column: int,
    weight_index_column: int,
    edge_threshold: float
) -> Callable[[nx.Graph, MetadataTypeRegistry], Callable[[List[str]], None]]:
    def _configure_graph_and_type_registry(
        graph: nx.Graph,
        type_registry: MetadataTypeRegistry  # the from_dataset contract will require this, but we don't need to use it
    ) -> Callable[[List[str]], None]:
        def _project_edges_above(row: List[str]):
            # since we already know everything there is to know about this data format, we don't need to
            # protect ourselves with length checks or anything like that.  our data is flawless!
            # but if it wasn't flawless, here is where you should handle it, by either adding nothing to the graph,
            # or adding what you feel you safely can
            source = row[source_index_column]
            target = row[target_index_column]
            weight = float(row[weight_index_column])
            if weight >= edge_threshold:
                graph.add_edge(source, target, weight=weight)
        return _project_edges_above
    return _configure_graph_and_type_registry
    

def _determine_edge_cut_threshold(
    weight_index_column: int,
    iterator
) -> float:
    reader = csv.reader(iterator, dialect="excel-tab")
    next(reader) # skip the header
    weights: List[float] = []
    for row in reader:
        weights.append(float(row[weight_index_column]))
        
    total_count = len(weights)
    
    histogram, bin_edges = np.histogram(weights)
    # we will take no more than the top 50%
    # note that this is probably a poor heuristic for almost any purpose, but it shows the process well enough
    bucket_sums = 0
    for i, bucket in enumerate(histogram):
        bucket_sums += bucket
        if bucket_sums >= total_count / 2:
            return bin_edges[i+1]
    raise Exception("More than 50% of the edge weights are all in a single bucket!")  


with open("/path/to/huge_edges_file.tsv", "r") as edge_file:
    where_to_cut, to_cut = tee(edge_file)
    edge_cut_threshold = _determine_edge_cut_threshold(2, where_to_cut)
    del where_to_cut
    csv_dataset = CsvDataset(
        source_iterator=to_cut,
        has_headers=True,
        dialect="excel-tab"
    )
    graph, _ = from_dataset(
        csv_dataset,
        _only_edges_above(3, 4, 2, edge_cut_threshold)
    )

```

There's a lot to unpack here, so let's walk through it:

- First we need to tee off the TextIO - we want to be able to walk through this file with two independent iterators and 
not impact each other.  We could also just read the file for reading twice, but we `tee`d instead.
- Next we call a function that iterates through the file.  This function does a very dirty job of:
    - Making a csv reader, using the same dialect we expect the file to be in
    - Skips the header row manually
    - Reads and converts every weight value to a float, then puts it into a list
    - Calls numpy's `histogram` function to generate a histogram of the weights and the edges at which each bin exists
    - Iterates through all of the histogram counts, summing (as it goes) the current number of weights in a given 
    bucket.  Once that sum is at or more than half the total number of weights, we take the right bin edge value and
    return it.  If, somehow, we get to the end, it means every weight is in the very last bucket, which means this 
    function will flat out fail.  For quick and dirty, it should work, but you may want more rigor in your edge cut
    threshold selection
- Presuming we have the edge cut threshold, we follow the normal process, only we iterate over the second of the `tee`d
iterators (as the first has already been exhausted - and indeed, deleted).
- We then call from_dataset, with an edge projection function that takes in the location of the source, target, and 
weight columns, as well as what edge_cut_threshold to use to determine whether we should keep the row.
- `from_dataset` is happy to use this function for every row it processes, determining whether to actually add the edge
to the graph or not. 

By following a general process like this, you can avoid loading large amounts of data into memory, only to cut it after 
the fact via the `networkx.Graph` api instead.

## But What About Vertex Metadata?
Up until now, we've only considered how to go about loading the edges of a graph and their associated weights and 
other metadata.

Graph vertices have metadata too, and both the `from_file` and `from_dataset` functions will help you with this.

`my_vertices.csv`
```
color,shape,id,enabled
blue,triangle,parent automotive company,1
green,square,automotive R&D X,1
red,circle,fabicatrix,0
teal,parallelogram,dwayne,0
```

Let's presume this file exists at the file path `/path/to/my_vertices.tsv`.  

**Note**: It's okay that your vertices have more or less information than your edges.  No errors will be thrown in this
process. 

#### `from_file` - with vertices
Very similar to the first example, vertex metadata can also be provided.  It even has two analogs to the 
`edge_metadata_behavior` values, `single` and `metadata`.  `none` is left out of the defaults because if one does not 
want vertex metadata, one shouldn't worry about processing another file for vertex data at all!  (Note: if you still 
want to, you can - but you need to use the `from_dataset` function!)

The following example is almost identical to the simple edge example.

```
08:01	2019-01-02	58	widgets, inc.	big box enterprises
08:03	2019-01-02	103	widgets, inc.	blue big box corp
08:03	2019-01-02	1000	widgets, inc.	fabricatrix
08:04	2019-01-02	5	ferrous machine company	widgets, inc.
08:04	2019-01-02	300	ferrous machine company	automotive R&D X
08:05	2019-01-02	10	parent automotive company	automotive R&D X
08:07	2019-01-02	10	parent automotive company	Your Local Auto Dealer
08:07	2019-01-03	2	parent automotive company	Your Local Auto Dealer
```

```python
import networkx as nx
from topologic.io import from_file, GraphContainer

with open("/path/to/my_edges.tsv", "r") as edge_file:
    with open("/path/to/my_vertices.csv", "r") as vertex_file:
        graph_container: GraphContainer = from_file(
            edge_csv_file=edge_file,
            source_column_index=3,  # note that we start counting from 0.  
            target_column_index=4,
            weight_column_index=2,
            edge_csv_has_headers=True,
            edge_dialect="excel-tab",
            edge_metadata_behavior="none",
            vertex_csv_file=vertex_file,
            vertex_column_index=2,
            vertex_csv_has_headers=True,
            vertex_dialect="excel",
            vertex_metadata_behavior="single"
        )
    
graph: nx.Graph = graph_container.graph
```

That was it.  All we did was take the information necessary to load a different csv file, with different parameters, and
the `from_file` function was able to take it from there.  Keen eyes will note that we also switched to a `csv` format
rather than a `tsv` format, and the dialect changed accordingly.

If you take the time to load this example up and run it yourself, you should find that the following nodes did not have
any metadata added for them:
- widgets, inc
- big box enterprises
- blue big box corp
- ferrous machine company
- Your Local Auto Dealer

Further, the vertex `dwayne` was not added - it had no edges, so we didn't bother to add it.  If that behavior isn't
what you'd like, read on to the next section!

#### `from_dataset` - with vertices

Like we said before, `from_file` is a pretty basic helper function around `from_dataset`.  However, when it comes to
vertex metadata, it's actually a helper function around two separate calls to `from_dataset`.

The `from_dataset` function doesn't know anything at all about whether we're adding edges or vertices.  In fact, it 
doesn't even need to care if we're adding nothing at all or **removing** vertices or edges!  That job is solely up to
the projection function provided to it.  

The following example is, once again, a very short replication of the `from_file` vertex example above.  The key 
to note is that, while you don't need to pass in graph object the first time, you *must* pass the same graph object 
returned from the edge-related `from_dataset` call, or else you'll end up with two disconnected graph objects, the
second of which is utterly empty.

```python
from topologic.io import CsvDataset, from_dataset
from topologic.projection import edge_ignore_metadata, vertex_with_single_metadata

with open("/path/to/my_edges.tsv", "r") as edge_file:
    with open("/path/to/my_vertices.csv", "r") as vertex_file:
        edge_csv_dataset = CsvDataset(
            source_iterator=edge_file,
            has_headers=True,
            dialect="excel-tab"
        )
        
        edge_projection_function = edge_ignore_metadata(
            source_index=3, 
            target_index=4, 
            weight_index=2
        )
        
        graph, _ = from_dataset(
            csv_dataset=edge_csv_dataset,
            projection_function_generator=edge_projection_function
        )  # if a graph object is not provided, this function creates one for you and returns it
        
        vertex_csv_dataset = CsvDataset(
            source_iterator=vertex_file,
            has_headers=True,
            dialect="excel"
        )
        
        vertex_projection_function = vertex_with_single_metadata(
            vertex_csv_dataset.headers(),
            2
        )
        
        updated_graph, _ = from_dataset(
            csv_dataset=vertex_csv_dataset,
            projection_function_generator=vertex_projection_function,
            graph=graph
        )
        # updated_graph and graph are references to the exact same object!
```

So, you see, we called `from_dataset` a second time, with a different CsvDataset and a different projection function.
We also passed in the previously generated graph object, so we were making sure we updated the same graph in place.

## Final Thoughts
There is nothing to stop you from calling `from_dataset` over the same graph object repeatedly.  It is not necessary for
you to spend your time pre-processing various sources of data into the same output file.  You can change the functions
used to project this data based on the format of the file, vs. translating the file into one common format.  Truthfully,
you're already doing that by turning `csv` families of files into a `networkx.Graph` object.

### MetadataTypeRegistry
You may have seen this referenced in the import lists in a few places.

The MetadataTypeRegistry, if you want it, will keep track of every attribute.  It attempts to type things in widening 
precision from `int` to `float` to `str`.  This may not be useful to you, but it may allow you to check and see if you 
can safely use another attribute to run calculations over, without having to iterate through every attribute on 
every single edge or vertex in the entire graph again.  You are also free to safely ignore it.
