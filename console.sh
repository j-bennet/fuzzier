#!/usr/bin/env bash

PYSPARK_PYTHON=$(which python) PYSPARK_DRIVER_PYTHON=$(which ipython) pyspark \
--master local[4] \
--driver-memory 16g \
--driver-java-options "-Droot.logger=ERROR,console"
