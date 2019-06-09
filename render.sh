#!/bin/bash

set -e

../pbrt-v3-build-release/pbrt main.pbrt
exrdisplay main.exr &
