#! /usr/bin/bash

model_name=$1
replaced_model_name=${model_name//\//__}

cd ../lm-evaluation-harness
lm_eval --model hf --model_args pretrained="$model_name",dtype="$2" --num_fewshot "$3" --tasks goat --device cuda --output_path "results/$replaced_model_name" --log_samples

cd ../leaderboard_evaluation
python add_result.py "../lm-evaluation-harness/results/$replaced_model_name/results.json"
