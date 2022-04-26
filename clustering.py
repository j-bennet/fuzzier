import time
import datetime as dt
from pprint import pprint
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from ratios import soundex_ratio, metaphone_ratio, fuzzy_ratio
from rapidfuzz import process, fuzz
from sklearn.cluster import AffinityPropagation


def make_clusters_affinity(texts):
    distance_matrix = pdist(
        texts.reshape((-1, 1)), lambda x, y: fuzzy_ratio(x[0], y[0])
    )
    square_matrix = squareform(distance_matrix)

    for i in range(len(texts)):
        square_matrix[i][i] = 100

    affprop = AffinityPropagation(
        affinity="precomputed",
        damping=0.99,
        verbose=True,
        random_state=0,
        max_iter=1_000,
    )
    affprop.fit(square_matrix)
    return affprop, square_matrix


def timeme(func):
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        res = func(*args, **kwargs)
        elapsed = dt.timedelta(seconds=(time.monotonic() - start))
        print(f"{func} took {str(elapsed)}")
        return res
    return wrapper


@timeme
def _calculate_similarity(texts):
    return process.cdist(texts, texts, scorer=fuzz.WRatio, workers=4)


@timeme
def _make_clusters(sim, cutoff=None):
    dfs = pd.DataFrame(sim, columns=texts, index=texts)
    dfs = dfs.rename_axis("s1").reset_index()
    dfs = dfs.melt(id_vars=["s1"], var_name="s2", value_name="sim")
    if cutoff is not None:
        dfs = dfs[(dfs["sim"] > cutoff)]
    dfs = (dfs
           .groupby("s1")
           .filter(lambda g: len(g) > 1)
           .groupby("s1")["s2"]
           .agg(lambda x: tuple(sorted(x)))
           .unique())
    return dfs


@timeme
def _print_clusters(dfs):
    for i, cluster in enumerate(dfs):
        print(f"Cluster #{i} with {len(cluster)} items")
        # pprint(cluster[:10])
    print("-" * 40)
    print(f"Clusters: {len(dfs)}")


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
def main(texts):
    sim = _calculate_similarity(texts)
    dfs = _make_clusters(sim, 90)
    _print_clusters(dfs)


if __name__ == "__main__":
    num_records = None
    df = pd.read_csv("nccs.csv", nrows=num_records)
    texts = df["address"].to_list()
    # texts = [
    #         "Petr",
    #         "Piotr",
    #         "Pyotr",
    #         "Michael",
    #         "Misha",
    #         "Michelle",
    #         "Ivan",
    #         "Evan",
    #         "Owen",
    #     ]
    main(texts)
