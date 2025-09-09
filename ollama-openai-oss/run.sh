#!/bin/bash

# Create a persistent volume to store Ollama models
podman volume create ollama_data

# Run the Ollama container in detached mode
# It will automatically expose port 11434
podman run \
  --replace \
  --name ollama-gpt-oss \
  -d \
  --device nvidia.com/gpu=all \
  --security-opt=label=disable \
  -p 11434:11434 \
  -v ollama_data:/root/.ollama \
  ollama-gpt-oss

# --- RELIABLE HEALTH CHECK ---
# Poll the Ollama API until it's ready, instead of using a fixed sleep.
echo "Waiting for Ollama server to be ready..."
while ! curl --silent --fail --output /dev/null http://localhost:11434/; do
    # Print a dot to show progress without spamming the console
    printf '.'
    sleep 1
done
# Print a newline for cleaner output after the dots
printf '\nOllama server is ready.\n'
# --- END HEALTH CHECK ---


# Pull the model into the running container
# This command is recommended by the provided research for easy setup
echo "Pulling the gpt-oss-20b model. This may take some time..."
podman exec ollama-gpt-oss ollama pull gpt-oss:20b

echo "Setup complete. The model is ready to be served."
