import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# The function now accepts 'model_path' instead of 'model_id'
def quantize_awq(model_path, quant_path):
    """
    Performs AWQ quantization using the autoawq library.
    """
    from awq import AutoAWQForCausalLM
    print(f"INFO: Starting AWQ quantization for model at {model_path}")

    # Quantization-specific parameters
    bits = int(os.environ.get("BITS", 4))
    group_size = int(os.environ.get("GROUP_SIZE", 128))
    quant_config = {"w_bit": bits, "q_group_size": group_size, "zero_point": True}
    print(f"INFO: AWQ config: {quant_config}")

    # Load model and tokenizer from the local model_path
    model = AutoAWQForCausalLM.from_pretrained(model_path, **{"low_cpu_mem_usage": True})
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    print("INFO: Base model and tokenizer loaded.")

    # Perform quantization
    model.quantize(tokenizer, quant_config=quant_config)
    print("INFO: Quantization complete.")

    # Save quantized model
    model.save_quantized(quant_path)
    tokenizer.save_pretrained(quant_path)
    print(f"INFO: AWQ model saved to {quant_path}")


# The function now accepts 'model_path' instead of 'model_id'
def quantize_gptq(model_path, quant_path):
    """
    Performs GPTQ quantization using the auto-gptq library.
    """
    from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
    print(f"INFO: Starting GPTQ quantization for model at {model_path}")

    # Quantization-specific parameters
    bits = int(os.environ.get("BITS", 4))
    group_size = int(os.environ.get("GROUP_SIZE", 128))
    quantize_config = BaseQuantizeConfig(
        bits=bits,
        group_size=group_size,
        desc_act=False, # Set to False for faster and often acceptable quantization
    )
    print(f"INFO: GPTQ config: bits={bits}, group_size={group_size}")

    # Load model and tokenizer from the local model_path
    model = AutoGPTQForCausalLM.from_pretrained(model_path, quantize_config, trust_remote_code=True, low_cpu_mem_usage=True)
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    print("INFO: Base model and tokenizer loaded.")

    # Prepare a sample dataset for calibration (required by GPTQ)
    # Using a simple, generic dataset for broad applicability.
    examples = [
        tokenizer("auto-gptq is a library for model quantization")
    ]
    print("INFO: Starting calibration...")

    # Perform quantization
    model.quantize(examples)
    print("INFO: Quantization complete.")

    # Save quantized model
    model.save_quantized(quant_path, use_safetensors=True)
    tokenizer.save_pretrained(quant_path)
    print(f"INFO: GPTQ model saved to {quant_path}")


if __name__ == "__main__":
    # The script now looks for a local MODEL_PATH inside the container
    model_path = os.environ.get("MODEL_PATH")
    quant_method = os.environ.get("QUANT_METHOD", "gptq").lower()
    output_dir = os.environ.get("OUTPUT_DIR", "/app/quantized_model")

    if not model_path:
        raise ValueError("FATAL: Environment variable MODEL_PATH must be set.")

    # Construct the full path for the quantized model output
    model_name = os.path.basename(model_path)
    quant_path = os.path.join(output_dir, f"{model_name}-{quant_method}")

    print("--- LLM Quantization Container ---")
    print(f"Model Path: {model_path}")
    print(f"Quantization Method: {quant_method.upper()}")
    print(f"Output Path: {quant_path}")
    print("---------------------------------")

    # Pass the local model_path to the appropriate function
    if quant_method == "awq":
        quantize_awq(model_path, quant_path)
    elif quant_method == "gptq":
        quantize_gptq(model_path, quant_path)
    else:
        raise ValueError(f"FATAL: Unknown quantization method '{quant_method}'. Use 'awq' or 'gptq'.")

    print("--- Quantization Task Finished ---")
