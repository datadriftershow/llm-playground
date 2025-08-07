curl http://localhost:8000/v1/completions -H "Content-Type: application/json" -d "{
  \"model\": \"/app/models/gpt-oss-20b\",
  \"prompt\": \"$(cat prompt.txt)\",
  \"max_tokens\": 2000,
  \"temperature\": 0.4,
  \"repetition_penalty\": 1.15
}"
#  \"stop\": [\"\n\"]
