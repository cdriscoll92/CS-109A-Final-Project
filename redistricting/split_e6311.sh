#!/bin/sh

SOURCE_FILE="e6311_post1948.csv"
OUTPUT_FILE="e6311_post1948-shapeless.csv"

cat $SOURCE_FILE | cut -d ',' -f 1-13 > $OUTPUT_FILE
