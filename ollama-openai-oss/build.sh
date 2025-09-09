#!/bin/bash

# Build the container image using the official ollama base
podman build --no-cache --pull -t ollama-gpt-oss .
