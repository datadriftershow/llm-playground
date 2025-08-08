curl http://localhost:8000/v1/completions -H "Content-Type: application/json" -d "{
  \"model\": \"/root/.cache/huggingface/gpt-oss-20b\",
  \"prompt\": \"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nExplain quantum entanglement in simple terms.<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n\",
  \"max_tokens\": 2048,
  \"temperature\": 0.0,
  \"repetition_penalty\": 1.15,
  \"stop\": [\"<|eot_id|>\", \"<|end_header_id|>\", \"\\n\\n\\n\"],
  \"frequency_penalty\": 0.2,
  \"presence_penalty\": 0.1
}"
  # \"stop\": [\"\n\"],
