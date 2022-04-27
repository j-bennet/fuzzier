import time
import datetime as dt
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import SQLContext
from pprint import pprint


def initialize(num_partitions=None):
    """Returns SparkContext and SQLContext."""
    conf = SparkConf()
    extra_settings = [
        ("spark.serializer", "org.apache.spark.serializer.KryoSerializer"),
        ("spark.executor.extraJavaOptions", "-XX:+UseG1GC"),
    ]
    if num_partitions:
        extra_settings.append(("spark.default.parallelism", num_partitions))

    conf.setAll(extra_settings)
    environment = {"PYTHON_EGG_CACHE": "/tmp/python-eggs"}
    sc = SparkContext(conf=conf, environment=environment)

    sqlContext = SQLContext(sc)
    if num_partitions:
        sqlContext.setConf("spark.sql.shuffle.partitions", num_partitions)

    jvm_logger = sc._jvm.org.apache.log4j
    jvm_logger.LogManager.getLogger("org").setLevel(jvm_logger.Level.ERROR)
    jvm_logger.LogManager.getLogger("akka").setLevel(jvm_logger.Level.ERROR)
    return sc, sqlContext


def distance_or_none(row, *, min_similarity=65):
    if min_similarity is None:
        return row[0].address, [row[1].address]
    if row[0].address == row[1].address:
        return row[0].address, [row[1].address]
    from rapidfuzz import fuzz
    ratio = fuzz.token_sort_ratio(row[0].address, row[1].address)
    if ratio >= min_similarity:
        return row[0].address, [row[1].address]
    return None


def main(sc, sqlContext, *, num_rows=None, num_partitions=None, min_similarity=None):
    start = time.monotonic()
    df = sqlContext.read.option("header", "true").csv("nccs.csv")
    if num_rows is not None:
        df = df.limit(num_rows)
    df = df.select(["address"])

    if num_partitions is not None:
        df = df.repartition(num_partitions)
    res = (
        df.rdd.cartesian(df.rdd)
        .filter(lambda x: x[0].address <= x[1].address)
        .map(lambda x: distance_or_none(x, min_similarity=min_similarity))
        .filter(lambda x: x is not None)
        .reduceByKey(lambda x, y: x + y)
        .filter(lambda x: len(x[1]) > 1)
        .collect()
    )
    elapsed = dt.timedelta(seconds=(time.monotonic() - start))
    # for i, (k, vs) in enumerate(res[:10]):
    #     print(f"Cluster {i} ({len(vs)})")
    #     pprint(vs)
    print(f"Records: {num_rows or df.count()}")
    print(f"Clusters: {len(res)}")
    print(f"Elapsed: {str(elapsed)}")


if __name__ == "__main__":
    partitions = 4
    min_similarity = 70
    rows = None
    sc, sqlContext = initialize(num_partitions=partitions)
    main(sc, sqlContext, num_rows=rows, num_partitions=partitions, min_similarity=min_similarity)
