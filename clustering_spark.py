import time
import datetime as dt
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import SQLContext


def initialize(target_partitions=None):
    """Returns SparkContext and SQLContext."""
    conf = SparkConf()
    extra_settings = [
        ("spark.serializer", "org.apache.spark.serializer.KryoSerializer"),
        ("spark.executor.extraJavaOptions", "-XX:+UseG1GC"),
    ]
    if target_partitions:
        extra_settings.append(("spark.default.parallelism", target_partitions))

    conf.setAll(extra_settings)
    environment = {"PYTHON_EGG_CACHE": "/tmp/python-eggs"}
    sc = SparkContext(conf=conf, environment=environment)

    sqlContext = SQLContext(sc)
    if target_partitions:
        sqlContext.setConf("spark.sql.shuffle.partitions", target_partitions)

    jvm_logger = sc._jvm.org.apache.log4j
    jvm_logger.LogManager.getLogger("org").setLevel(jvm_logger.Level.ERROR)
    jvm_logger.LogManager.getLogger("akka").setLevel(jvm_logger.Level.ERROR)
    return sc, sqlContext


def distance(row):
    from rapidfuzz import fuzz

    return (
        row[0].address,
        row[1].address,
        fuzz.token_sort_ratio(row[0].address, row[1].address),
    )


def main(sc, sqlContext, num_rows=None):
    start = time.monotonic()
    df = (
        sqlContext.read.option("header", "true")
        .csv("nccs.csv")
        .limit(num_rows)
        .select(["address"])
    )
    cnt = df.rdd.cartesian(df.rdd).map(lambda x: distance(x)).count()
    elapsed = dt.timedelta(seconds=(time.monotonic() - start))
    print(f"Count: {cnt}, elapsed: {str(elapsed)}")


if __name__ == "__main__":
    sc, sqlContext = initialize(target_partitions=32)
    main(sc, sqlContext, num_rows=10000)
