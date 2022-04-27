#!/usr/bin/env bash

#--driver-memory 4g \
#--executor-memory 4g \
#--num-executors 2 \
#--executor-cores 4 \
#--conf "spark.executor.memoryOverhead=2g" \

PYSPARK_PYTHON=$(which python) PYSPARK_DRIVER_PYTHON=$(which python) spark-submit \
--master "local[*]" \
--driver-java-options "-Droot.logger=ERROR,console" \
clustering_spark.py