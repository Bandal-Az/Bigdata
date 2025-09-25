#!/bin/bash

python -m torch.distributed.launch --nproc_per_node=1\
    /workspace/AttrNet/scene_parse/attr_net/tools/run_train.py \
    --dataset nia80 --num_iters 50000 \
    --run_dir /workspace/run/attr_net/train \
    --batch_size 32 --learning_rate 0.001 \
    --num_workers 1 --val_epochs 5 --feature_vector_len 26 \
    --dataset_dir /workspace/data/dataset