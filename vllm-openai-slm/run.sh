podman run --gpus all \
  --name vllm-gpt-oss-20b \
  --shm-size=10g \
  --device nvidia.com/gpu=all \
  --security-opt=label=disable \
  --replace \
  -p 8000:8000 \
  -v /home/mentat/workspace/models:/root/.cache/huggingface \
  --env TRANSFORMERS_OFFLINE=1 \
  --env PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
  vllm/vllm-openai:gptoss \
  --model /root/.cache/huggingface/gpt-oss-20b \
  --host 0.0.0.0 \
  --port 8000 \
  --max-model-len 15000 \
  --gpu-memory-utilization 0.93 \
  --dtype auto \
  --max-num-seqs 1 \
  --trust-remote-code
  # --env VLLM_ATTENTION_BACKEND=TRITON_ATTN_VLLM_V1 \
