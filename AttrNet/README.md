진행 순서

1. 이미지 리사이즈
    ``` bash
    python resize.py
    ```
2. yolo annotation 생성
    ``` bash
    python yolov5/mask_yolo_ann_txt_all.py
    ```
3. annotation file copy
    ```
    cp ./data/yolo/ann/* ./data/jpg-480/train
    rm -r ./data/yolo/ann
    ```
4. yolo train
    ``` bash
        yolov5/sbatch_yolo_basketball.sh
    python ./yolov5/train.py --img 480 --batch 1600 --epochs 100 --data ./yolov5/data/nia_all.yaml --weights yolov5s.pt --device 0 --project ./data/yolo/train --workers 16
    ```
5. yolo inference
    ``` bash
        yolov5/sbatch_yolo_basketball_test.sh

    python ./yolov5/detect.py --weights yolov5s.pt --source ./data/jpg-480/train --project ./data/yolo/detect --device 0 --data ./yolov5/data/nia_all.yaml --img 480 --save-txt
    python ./yolov5/detect.py --weights /workspace/data/yolo/train/exp/weights/best.pt --source ./data/jpg-480/train --project ./data/yolo/detect --device 0 --data ./yolov5/data/nia_all.yaml --img 480 --save-txt
    ```
6. txt copy
    ```
    mkdir ./data/yolo-ann
    cp ./data/yolo/detect/exp/labels/* ./data/yolo-ann
    ```
5. ns-vqa annotation 생성
    ``` bash
    python ./attnet/annotations/make_ann_yolo_to_attnet_all.py
    ```
6. ns-vqa train
    ``` bash
    sh attnet/train.sh
    ```
7. ns-vqa test
    ``` bash
    python ./attnet/scene_parse/attr_net/tools/run_test_for_acc.py --num_worker 16 --geature_vector_len 102 --dataset basketball --run_dir ./data/jpg-480 --load_checkpoint_path /workspace/model/attnet-final-100e-ckpt.pt --basketball_ann_path /workspace/data/attnet_final_annotations.json --basketball_img_dir ./data/jpg-480 --split_id 175216 --batch_size 32
    ```