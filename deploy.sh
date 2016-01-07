#!/bin/bash

docker login
docker build -t romlinch/$(basename $(pwd)) .
docker tag romlinch/$(basename $(pwd)):latest romlinch/$(basename $(pwd)):$(git describe --always --tags)
docker push romlinch/$(basename $(pwd))
docker push romlinch/$(basename $(pwd)):$(git describe --always --tags)

