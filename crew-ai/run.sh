#!/bin/bash
#
# Run the CrewAI container on the same network
podman run \
  --replace \
  --name crewai-hello-world \
  --network host \
  --rm \
  crewai-hello-world
