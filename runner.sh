#!/usr/bin/env bash

#--num-executors 2 \
#--executor-cores 4 \
#--executor-memory 4g \
#--conf "spark.executor.memoryOverhead=2g" \

PYSPARK_PYTHON=$(which python) PYSPARK_DRIVER_PYTHON=$(which python) spark-submit \
--master "local[*]" \
--driver-memory 24g \
--driver-java-options "-Droot.logger=ERROR,console" \
clustering_spark.py