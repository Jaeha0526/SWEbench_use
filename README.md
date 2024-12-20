# SWE-bench Evaluation with Toolformer Support

This repository contains modified SWE-bench evaluation code that incorporates Toolformer functionality, allowing for tool usage during model inference.

## Overview

The evaluation process consists of three main components:

1. Model Inference
2. Data Type Conversion
3. Evaluation Running

### 1. Model Inference on SWE-bench

The inference process takes issues and codebases as input, generating diff files as solutions. When Toolformer is enabled, the system can detect and execute tool calls during inference.

#### Without Tool Usage

To run inference without tool usage (example using gpt-4o-mini on SWE-bench_oracle data):

```bash
python -m swebench.inference.run_api_toolformer \
    --dataset_name_or_path princeton-nlp/SWE-bench_oracle \
    --model_name_or_path gpt-4o-mini \
    --output_dir ./outputs \
    --split dev \
    --my_set test
```

#### With Tool Usage

To run inference with Toolformer support (example using finetuned gpt-4o-mini):

```bash
python -m swebench.inference.run_api_toolformer \
    --dataset_name_or_path princeton-nlp/SWE-bench_oracle \
    --model_name_or_path ft:gpt-4o-mini-2024-07-18:personal:toolformer-mistral:AfWBG2x5 \
    --output_dir ./outputs \
    --split dev \
    --my_set test \
    --toolformer
```

### 2. Data Type Conversion

Convert the inference outputs to the required format for evaluation.

#### Without Tool Usage Example:

```bash
python convert_predictions.py \
    --input_file ./outputs/gpt-4o-mini__SWE-bench_oracle__dev__test.jsonl \
    --output_file ./converted_outputs/gpt-4o-mini_wo_tool_use_oracle_dev_test.json
```

#### With Tool Usage Example:

```bash
python convert_predictions.py \
    --input_file ./outputs/ft:gpt-4o-mini-2024-07-18:personal:toolformer-mistral:AfWBG2x5__SWE-bench_oracle__dev__test.jsonl \
    --output_file ./converted_outputs/ft_codeLlama_wo_tool_use_oracle_dev_test.json
```

### 3. Running Evaluation

The evaluation phase applies the model's patch suggestions and verifies if the issues are resolved.

#### Without Tool Usage Example:

```bash
python -m swebench.harness.run_evaluation \
    --dataset_name princeton-nlp/SWE-bench_oracle \
    --predictions_path ./converted_outputs/gpt-4o-mini_wo_tool_use_oracle_dev_testtest.json \
    --max_workers 6 \
    --split dev \
    --run_id gpt-4o-mini_wo_tool_use_oracle_dev_test
```

#### With Tool Usage Example:

```bash
python -m swebench.harness.run_evaluation \
    --dataset_name princeton-nlp/SWE-bench_oracle \
    --predictions_path ./converted_outputs/ft_codeLlama_wo_tool_use_oracle_dev_test.json \
    --max_workers 6 \
    --split dev \
    --run_id ft_codeLlama_wo_tool_use_oracle_dev_test
```

## Note

When the `--toolformer` flag is enabled, the system will detect and execute tool calls during the inference process, allowing for dynamic tool usage while generating solutions.