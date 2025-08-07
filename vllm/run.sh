podman run \
  --replace \
  --name vllm \
  --device nvidia.com/gpu=all \
  --security-opt=label=disable \
  --shm-size=10g \
  -p 8000:8000 \
  -v /home/mentat/workspace/llm-hello-world/models:/app/models \
  vllm
