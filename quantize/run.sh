podman run --rm \
  --device nvidia.com/gpu=all \
  --security-opt=label=disable \
  -v ./quantized-models:/app/quantized_model \
  -v /home/mentat/workspace/models:/app/models \
  -e MODEL_PATH="/app/models/Skywork-o1-Open-Llama-3.1-8B" \
  -e QUANT_METHOD="awq" \
  -e BITS="4" \
  -e GROUP_SIZE="128" \
  llm-quantizer-app
