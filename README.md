### Simplified clustering of 23609 addresses

Reads a csv with `url,name,address` of Ripe NCC entities.

Creates a graph where keys are indices of NCCs that have "neigbors" selected by address similarity.
The graph looks like this:

```python
graph = {
    1: [2, 4],
    2: [1],
    4: [1]
}
```

In the case above, the script will output that it found 3 clusters. Notice that it counts
links in both directions. Node 1 is linked to node 2, but node 2 is also linked to node 1.

The graph is sparse, nodes with no neighbors are not included.

Script output with tf-idf (https://bergvca.github.io/2017/10/14/super-fast-string-matching.html):

```
$ python clustering.py
Processing 23609 records
<function _make_graph at 0x13116d598> took 0:00:00.097024
<function _make_clusters_tfidf at 0x13116d6a8> took 0:00:03.565581
<function make_graph at 0x13116d9d8> took 0:00:03.565625
----------------------------------------
Clusters: 6197
<function print_graph at 0x13116d8c8> took 0:00:00.000010
Wrote output data to output.csv
```

With rapidfuzz takes 17 min (workers=8), MacBook Pro 2020, 2.3 GHz, 32Gb of RAM:

```
$ python clustering.py
Processing 23609 records
<function _make_graph at 0x139fc2510> took 0:00:00.747032
<function _make_clusters_ratio at 0x139fc2730> took 0:17:22.536067
<function make_graph at 0x139fc2950> took 0:17:22.536154
----------------------------------------
Clusters: 9442
<function print_graph at 0x139fc2840> took 0:00:00.000013
```

### Turning the knobs

A few settings are defined in `clustering.py` in `main`. Those are good to experiment with.

The script supports two methods to calculate similarity: `tf-idf` or `fuzz` (from `rapidfuzz` module). 

The threshhold of similarity is set as `min_similarity` (1-100) in `clustering.py`.

It's possible to set `num_records` in `clustering.py` to a smaller number of records, for easier testing.

`write_output` can be set to True or False.

`verbose` can be set to True or False, and will print all the graph nodes and their neighbors if True.

For scoring with `rapidfuzz`, scorer is set to `fuzz.token_sort_ratio`, but `fuzz.token_sort_ratio` looks pretty good as well.

### Result output

Result output is written to csv as follows:

```s1,s2,sim,i1,i2,name1,name2,url1,url2```

* s1 = address of the 1st NCC
* s1 = address of the 2nd NCC
* sim - similarity score
* i1 - index of the 1st NCC in `nccs.csv`
* i2 - index of the 2nd NCC in `nccs.csv`
* name1 - name of the 1st NCC in `nccs.csv`
* name2 - name of the 2nd NCC in `nccs.csv`
* url1 - index of the 1st NCC in `nccs.csv`
* url2 - index of the 2nd NCC in `nccs.csv`

Only records with `sim > min_similarity` are included.

### Possible improvements

Maybe use tf/idf with lower `min_similarity` (65?) as first stage, 
then fuzzy ratio with higher `min_similarity` as 2nd stage, to filter
out less likely candidates. Fuzzy ratio is slow, but if it's done
on smaller sets of nodes already discovered by tf/idf, it won't be so bad.
