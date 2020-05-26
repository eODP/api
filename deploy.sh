#!/bin/bash

rsync -av --progress --exclude={"__pycache__",".pytest_cache",".DS_Store","tests"} --rsh='ssh -p7000' ./app ./migrations $1:/data/eodp

