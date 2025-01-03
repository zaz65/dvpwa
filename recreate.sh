#!/bin/bash
set -e

podman compose down
podman volume ls -qf dangling=true | xargs -r podman volume rm
podman compose build
