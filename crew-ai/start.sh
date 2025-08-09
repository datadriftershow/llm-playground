#!/bin/bash

# Start the LiteLLM proxy in the background
echo "Starting LiteLLM Proxy..."
litellm --config /app/config.yaml --port 4000 &

# Give the proxy a moment to start up
sleep 5

# Run the main CrewAI application
echo "Starting CrewAI Application..."
python3 /app/main.py
