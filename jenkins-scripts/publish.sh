#!/usr/bin/env sh

echo $NODE_NAME
echo $PIPELINE_NODE
echo $RESERVE
set -ex
echo "$BRANCH_NAME"

make build
make publish
