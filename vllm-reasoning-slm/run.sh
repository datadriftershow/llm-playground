podman run \
  --replace \
  --name vllm-reasoning \
  --device nvidia.com/gpu=all \
  --security-opt=label=disable \
  --shm-size=10g \
  -p 8000:8000 \
  -v /home/mentat/workspace/models:/app/models \
  vllm-reasoning
