#!/bin/bash

python /workspace/AttrNet/scene_parse/attr_net/tools/run_test_for_acc.py --num_worker 1 \
    --feature_vector_len 26 \
    --dataset nia80 \
    --run_dir /workspace/run/attr_net/test \
    --load_checkpoint_path /workspace/run/attr_net/train/checkpoint_latest.pt \
    --batch_size 16 \
    --dataset_dir /workspace/data/dataset