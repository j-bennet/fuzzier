import datetime as dt
import re
import time

import numpy as np
import pandas as pd
import sparse_dot_topn.sparse_dot_topn as ct
from rapidfuzz import process, fuzz
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import OrderedDict


def ngrams(string, n=3):
    string = re.sub(r"[,-./\s]", r"", string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return ["".join(ngram) for ngram in ngrams]


def timeme(func):
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        res = func(*args, **kwargs)
        elapsed = dt.timedelta(seconds=(time.monotonic() - start))
        print(f"{func} took {str(elapsed)}")
        return res

    return wrapper


def cosine_similarity_top(A, B, *, top_n=None, lower_bound=0.0):
    """Cosine similarity between vectors. Limit to top n matches only."""
    A = A.tocsr()
    B = B.tocsr()
    M, _ = A.shape
    _, N = B.shape

    if top_n is None:
        top_n = N

    idx_dtype = np.int32

    nnz_max = M * top_n

    indptr = np.zeros(M + 1, dtype=idx_dtype)
    indices = np.zeros(nnz_max, dtype=idx_dtype)
    data = np.zeros(nnz_max, dtype=A.dtype)

    ct.sparse_dot_topn(
        M,
        N,
        np.asarray(A.indptr, dtype=idx_dtype),
        np.asarray(A.indices, dtype=idx_dtype),
        A.data,
        np.asarray(B.indptr, dtype=idx_dtype),
        np.asarray(B.indices, dtype=idx_dtype),
        B.data,
        top_n,
        lower_bound,
        indptr,
        indices,
        data,
    )

    return csr_matrix((data, indices, indptr), shape=(M, N))


def _unpack_cosine_matches(sparse_matrix, texts, top_n=100):
    """Take the sparce matrix of cosine similarities, and return a dataframe of matched text pairs."""
    non_zeros = sparse_matrix.nonzero()

    sparserows = non_zeros[0]
    sparsecols = non_zeros[1]

    if top_n:
        nr_matches = top_n
    else:
        nr_matches = sparsecols.size

    left_side = np.empty([nr_matches], dtype=object)
    right_side = np.empty([nr_matches], dtype=object)
    similairity = np.zeros(nr_matches)
    index1 = np.zeros(nr_matches)
    index2 = np.zeros(nr_matches)

    for index in range(0, nr_matches):
        left_side[index] = texts[sparserows[index]]
        right_side[index] = texts[sparsecols[index]]
        similairity[index] = sparse_matrix.data[index]
        index1[index] = int(sparserows[index])
        index2[index] = int(sparsecols[index])

    df = pd.DataFrame(
        data={
            "s1": left_side,
            "s2": right_side,
            "sim": similairity,
            "i1": index1,
            "i2": index2,
        }
    )
    df = df.astype({"i1": "int32", "i2": "int32"})
    df = df[df["i1"] != df["i2"]]
    return df


@timeme
def _make_graph(df):
    """Take the dataframe with text1, text2, similarity ratio,
    and make a sparce graph - a dict of text indices that looks like this
    {
        index1: [index2, index3],
        index2: [index1]
        index3: [index1]
        index4: None
    }
    """
    grouped = df.groupby("i1").agg({"i2": lambda x: set(x)}).reset_index().to_records()
    graph = OrderedDict()
    for (_, i1, i2) in grouped:
        graph[i1] = i2
    return graph


@timeme
def _make_clusters_tfidf(texts, min_similarity=None, top_n=100):
    """Uze tf/idf (fast) to calculate similarity"""
    vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)
    tf_idf_matrix = vectorizer.fit_transform(texts)
    matches = cosine_similarity_top(
        tf_idf_matrix,
        tf_idf_matrix.transpose(),
        top_n=top_n,
        lower_bound=(min_similarity / 100),
    )
    dfs = _unpack_cosine_matches(matches, texts, top_n=top_n)
    graph = _make_graph(dfs)
    return graph, dfs


@timeme
def _make_clusters_ratio(texts, min_similarity=None, scorer=None):
    """Uze fuzzy ratio (slow) to calculate similarity"""
    sim = process.cdist(texts, texts, scorer=scorer, workers=8)
    dfs = pd.DataFrame(sim)
    dfs = dfs.rename_axis("i1").reset_index()
    dfs = dfs.melt(id_vars=["i1"], var_name="i2", value_name="sim")
    dfs["s1"] = dfs["i1"].apply(lambda x: texts[x])
    dfs["s2"] = dfs["i2"].apply(lambda x: texts[x])
    dfs = dfs[dfs["i1"] != dfs["i2"]]
    if min_similarity is not None:
        dfs = dfs[(dfs["sim"] >= min_similarity)]
    graph = _make_graph(dfs)
    return graph, dfs


@timeme
def print_graph(g, df, verbose=False):
    if verbose:
        for k, vs in g.items():
            print(f"Node #{k} has {len(vs)} connection(s)")
            print(f"{k}: {df.loc[k, 'address']}, {df.loc[k, 'name']}")
            for v in vs:
                print(f"{v}: {df.loc[v, 'address']}, {df.loc[v, 'name']}")
    print("-" * 40)
    print(f"Clusters: {len(g)}")


@timeme
def make_graph(texts, *, min_similarity=None, method=None):
    """Make groups of texts (addresses) based on similarity"""
    print(f"Processing {len(texts)} records")
    if method == "fuzz":
        graph, dfs = _make_clusters_ratio(
            texts, min_similarity=min_similarity, scorer=fuzz.token_sort_ratio
        )
    elif method == "tf-idf":
        graph, dfs = _make_clusters_tfidf(
            texts, min_similarity=min_similarity, top_n=None
        )
    else:
        raise NotImplementedError(f"Don't know how to handle method: {method}. Known methods: fuzz, tf-idf")
    return graph, dfs


def save_results(dfs, *, df=None, filename="output.csv"):
    """Write grouped data to output file"""
    dfs["name1"] = dfs["i1"].apply(lambda x: df.loc[x, "name"])
    dfs["name2"] = dfs["i2"].apply(lambda x: df.loc[x, "name"])
    dfs["url1"] = dfs["i1"].apply(lambda x: df.loc[x, "url"])
    dfs["url2"] = dfs["i2"].apply(lambda x: df.loc[x, "url"])
    dfs = dfs.sort_values(["s1", "s2"])
    dfs.to_csv(filename, index=False)
    print(f"Wrote output data to {filename}")


if __name__ == "__main__":
    num_records = None
    min_similarity = 80
    write_output = True
    verbose = False
    method = "tf-idf"
    output_filename = f"output-{method}.csv"
    df = pd.read_csv("nccs.csv", nrows=num_records)
    texts = df["address"].to_list()
    graph, dfs = make_graph(texts, min_similarity=min_similarity, method=method)
    print_graph(graph, df, verbose=verbose)
    if write_output:
        save_results(dfs, df=df, filename=output_filename)
