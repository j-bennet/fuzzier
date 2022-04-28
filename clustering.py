import datetime as dt
import re
import time
from pprint import pprint

import numpy as np
import pandas as pd
import sparse_dot_topn.sparse_dot_topn as ct
from rapidfuzz import process, fuzz
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer


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


def _unpack_cosine_matches(sparse_matrix, texts, top=100):
    """Take the sparce matrix of cosine similarities, and return a dataframe of matched text pairs."""
    non_zeros = sparse_matrix.nonzero()

    sparserows = non_zeros[0]
    sparsecols = non_zeros[1]

    if top:
        nr_matches = top
    else:
        nr_matches = sparsecols.size

    left_side = np.empty([nr_matches], dtype=object)
    right_side = np.empty([nr_matches], dtype=object)
    similairity = np.zeros(nr_matches)

    for index in range(0, nr_matches):
        left_side[index] = texts[sparserows[index]]
        right_side[index] = texts[sparsecols[index]]
        similairity[index] = sparse_matrix.data[index]

    df = pd.DataFrame({"s1": left_side, "s2": right_side, "sim": similairity})
    df = df[df["s1"] <= df["s2"]]
    return df


@timeme
def _group_matches(df):
    """Take the dataframe with text1, text2, similarity ratio,
    and return grouped tuples of text2, each representing a cluster"""
    dfs = (
        df.groupby("s1")
        .filter(lambda g: len(g) > 1)
        .groupby("s1")["s2"]
        .agg(lambda x: tuple(sorted(x)))
        .unique()
    )
    return dfs


@timeme
def _make_clusters_tfidf(texts, min_similarity=None, top_n=100):
    vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)
    tf_idf_matrix = vectorizer.fit_transform(texts)
    matches = cosine_similarity_top(
        tf_idf_matrix,
        tf_idf_matrix.transpose(),
        top_n=top_n,
        lower_bound=(min_similarity / 100),
    )
    dfs = _unpack_cosine_matches(matches, texts, top=top_n)
    dfs = _group_matches(dfs)
    return dfs


@timeme
def _make_clusters_ratio(texts, min_similarity=None, scorer=None):
    sim = process.cdist(texts, texts, scorer=scorer, workers=8)
    dfs = pd.DataFrame(sim, columns=texts, index=texts)
    dfs = dfs.rename_axis("s1").reset_index()
    dfs = dfs.melt(id_vars=["s1"], var_name="s2", value_name="sim")
    if min_similarity is not None:
        dfs = dfs[(dfs["sim"] >= min_similarity)]
    dfs = _group_matches(dfs)
    return dfs


@timeme
def _print_clusters(dfs, verbose=False):
    if verbose:
        for i, cluster in enumerate(dfs):
            print(f"Cluster #{i} with {len(cluster)} items")
            pprint(cluster[:10])
    print("-" * 40)
    print(f"Clusters: {len(dfs)}")


# def make_clusters_affinity(texts):
#     distance_matrix = pdist(
#         texts.reshape((-1, 1)), lambda x, y: fuzzy_ratio(x[0], y[0])
#     )
#     square_matrix = squareform(distance_matrix)
#
#     for i in range(len(texts)):
#         square_matrix[i][i] = 100
#
#     affprop = AffinityPropagation(
#         affinity="precomputed",
#         damping=0.99,
#         verbose=True,
#         random_state=0,
#         max_iter=1_000,
#     )
#     affprop.fit(square_matrix)
#     return affprop, square_matrix


# def print_clusters(affprop, square_matrix, texts):
#     """Print clusters"""
#     print("Similarity matrix:")
#     print(square_matrix)
#
#     clusters = np.unique(affprop.labels_)
#     print(f"\n~ Number of texts:: {texts.shape[0]}")
#     print(f"~ Number of clusters:: {clusters.shape[0]}")
#     if clusters.shape[0] == 1:
#         print("No clusters found.")
#         return
#     for cluster_id in clusters:
#         text_indices = np.nonzero(affprop.labels_ == cluster_id)
#         cluster = sorted(texts[text_indices])
#         print(f"\n# Cluster ({cluster_id}) with ({len(cluster)}) elements")
#         pprint(cluster)
#


@timeme
def main(texts, *, min_similarity=None, method=None, verbose=False):
    print(f"Processing {len(texts)} records")
    if method == "fuzz":
        dfs = _make_clusters_ratio(
            texts, min_similarity=min_similarity, scorer=fuzz.WRatio
        )
    elif method == "tf-idf":
        dfs = _make_clusters_tfidf(texts, min_similarity=min_similarity, top_n=None)
    else:
        raise NotImplementedError(f"Don't know how to handle method: {method}")
    _print_clusters(dfs, verbose=verbose)


if __name__ == "__main__":
    num_records = None
    min_similarity = 60
    verbose = True
    df = pd.read_csv("nccs.csv", nrows=num_records)
    texts = df["address"].to_list()
    main(texts, min_similarity=min_similarity, method="tf-idf", verbose=verbose)
