#!/usr/bin/env bash

PYSPARK_PYTHON=$(which python) PYSPARK_DRIVER_PYTHON=$(which ipython) pyspark \
--master local[4] \
--driver-memory 6g \
--executor-memory 4g \
--num-executors 2 \
--executor-cores 4 \
--conf "spark.executor.memoryOverhead=2g" \
--driver-java-options "-Droot.logger=ERROR,console"
