#!/bin/bash

docker login
docker build -t $(basename $(pwd)) .
docker tag $(basename $(pwd)):latest $(basename $(pwd)):$(git describe --always --tags)
